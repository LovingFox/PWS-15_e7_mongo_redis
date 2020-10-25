from flask import Response, request, jsonify
from flask_restful import Resource
from mongoengine import Document, StringField, ListField
from flask_caching import Cache

cache = Cache()

def clear_cache(adv_id=None, advs=False):
    """
    Сбрасывает кэш выдачи отдельного объявления по _adv_id_ (его содержание и статистика)
    и всего списка с объявлениями (если _advs_ == true)
    """
    if adv_id:
        cache.delete('adv_' + adv_id)
        cache.delete('stat_' + adv_id)

    if advs:
        cache.delete('advs')


class Advert(Document):
    '''
    Модель объявления в базе Mongodb
    '''
    title = StringField(required=True)
    body = StringField(required=True)
    tags = ListField(StringField())
    comments = ListField(StringField())


class AdvertsApi(Resource):
    '''
    Вьюха для получения списка объявлений
    и создания нового объявления
    '''
    def get(self):
        try:
            # Если есть кэш, то возвращаем его
            c = cache.get('advs')
            if c:
                return c
        except: pass

        try:
            output = jsonify(Advert.objects())
            try:
                # Пишем в кэш список объявлений перед их возвращением в ответе
                cache.set('advs', output)
            except: pass
            return output
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        data = request.get_json()
        try:
            data['tags'] = set(data.get('tags', [])) # схлопываем повторяющиеся тэги
            adv = Advert(**data).save()
            try:
                # Удаляем даные из кэша, т.к. они обновились в базе
                clear_cache(advs=True)
            except: pass
            return {'id': str(adv.id)}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvertApi(Resource):
    '''
    Вьюха для получения одного объявления по его id
    и изменение/удаления объявления
    '''
    def get(self, adv_id: str):
        try:
            # Если есть кэш, то возвращаем его
            c = cache.get('adv_' + adv_id)
            if c:
                return c
        except: pass

        try:
            output = jsonify(Advert.objects.get(id=adv_id))
            try:
                # Пишем в кэш объявление перед возвращением его в ответе
                cache.set('adv_' + adv_id, output)
            except: pass
            return output
        except Exception as e:
            return {'message': str(e)}, 400

    def patch(self, adv_id: str):
        data = request.get_json()
        try:
            Advert.objects(id=adv_id).update_one(**data)
            try:
                # Удаляем даные из кэша по объявлению, т.к. оно обновились в базе
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": adv_id}
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, adv_id: str):
        try:
            count = Advert.objects(id=adv_id).delete()
            try:
                # Удаляем даные из кэша по объявлению, т.к. оно удалено в базе
                clear_cache(adv_id, advs=True)
            except: pass
            return {"deleted": count}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvTagsApi(Resource):
    '''
    Вьюха для добавления или удаления тэгов в объявление
    '''
    def post(self, adv_id: str):
        data = request.get_json()
        try:
            adv = Advert.objects(id=adv_id).first()
            # добавляем и схлопываем через set, что бы убрать дубликаты тэгов
            adv.tags = list(set(adv.tags + data.get('tags', [])))
            adv.save()
            try:
                # Удаляем даные из кэша по объявлению, т.к. оно обновились в базе
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": str(adv_id)}
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, adv_id: str):
        data = request.get_json()
        try:
            adv = Advert.objects(id=adv_id).first()
            # оставляем только разницу между имеющимися тэгами и удаляемыми
            adv.tags = list(set(adv.tags) - set(data.get('tags', [])))
            adv.save()
            try:
                # Удаляем даные из кэша по объявлению, т.к. оно обновились в базе
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": str(adv_id)}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvCommentApi(Resource):
    '''
    Вьюха только для добавления комментария в объявление
    '''
    def post(self, adv_id: str):
        data = request.get_json()
        try:
            adv = Advert.objects(id=adv_id).first()
            # обновляем список комментариев, добавляя новый
            adv.comments += [data.get('comment')]
            adv.save()
            try:
                # Удаляем даные из кэша по объявлению, т.к. оно обновились в базе
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": str(adv_id)}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvStatApi(Resource):
    '''
    Вьюха только для показа статистики объявления
    '''
    def get(self, adv_id: str):
        try:
            c = cache.get('stat_' + adv_id)
            if c:
                return c
        except: pass

        try:
            adv = Advert.objects(id=adv_id).first()
            output = {"tags": len(adv.tags), "comments": len(adv.comments)}
            try:
                # Пишем в кэш объявление перед возвращением его в ответе
                cache.set('stat_' + adv_id, output)
            except: pass
            return output
        except Exception as e:
            return {'message': str(e)}, 400
