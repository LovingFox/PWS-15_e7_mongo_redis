from flask import Response, request, jsonify
from flask_restful import Resource
from mongoengine import Document, StringField, ListField
from flask_caching import Cache

cache = Cache()

def clear_cache(adv_id=None, advs=False):
    if adv_id:
        cache.delete('adv_' + adv_id)
        cache.delete('stat_' + adv_id)

    if advs:
        cache.delete('advs')


class Advert(Document):
    title = StringField(required=True)
    body = StringField(required=True)
    tags = ListField(StringField())
    comments = ListField(StringField())


class AdvertsApi(Resource):
    def get(self):
        try:
            c = cache.get('advs')
            if c:
                return c
        except: pass

        try:
            output = jsonify(Advert.objects())
            try:
                cache.set('advs', output)
            except: pass
            return output
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        data = request.get_json()
        try:
            data['tags'] = set(data.get('tags', []))
            adv = Advert(**data).save()
            try:
                clear_cache(advs=True)
            except: pass
            return {'id': str(adv.id)}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvertApi(Resource):
    def get(self, adv_id: str):
        try:
            c = cache.get('adv_' + adv_id)
            if c:
                return c
        except: pass

        try:
            output = jsonify(Advert.objects.get(id=adv_id))
            try:
                cache.set('adv_' + adv_id, output)
            except: pass
            return output
        except Exception as e:
            return {'message': str(e)}, 400

    def patch(self, adv_id: str):
        data = request.get_json()
        try:
            count = Advert.objects(id=adv_id).update_one(**data)
            try:
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": adv_id}
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, adv_id: str):
        try:
            count = Advert.objects(id=adv_id).delete()
            try:
                clear_cache(adv_id, advs=True)
            except: pass
            return {"deleted": count}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvTagsApi(Resource):
    def post(self, adv_id: str):
        data = request.get_json()
        try:
            adv = Advert.objects(id=adv_id).first()
            adv.tags = list(set(adv.tags + data.get('tags', [])))
            adv.save()
            try:
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": str(adv_id)}
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, adv_id: str):
        data = request.get_json()
        try:
            adv = Advert.objects(id=adv_id).first()
            adv.tags = list(set(adv.tags) - set(data.get('tags', [])))
            adv.save()
            try:
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": str(adv_id)}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvCommentApi(Resource):
    def post(self, adv_id: str):
        data = request.get_json()
        try:
            adv = Advert.objects(id=adv_id).first()
            adv.comments += [data.get('comment')]
            adv.save()
            try:
                clear_cache(adv_id, advs=True)
            except: pass
            return {"updated": str(adv_id)}
        except Exception as e:
            return {'message': str(e)}, 400


class AdvStatApi(Resource):
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
                cache.set('stat_' + adv_id, output)
            except: pass
            return output
        except Exception as e:
            return {'message': str(e)}, 400
