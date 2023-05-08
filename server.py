from sqlalchemy.exc import IntegrityError

from models import Session, Ad
from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask('app')

class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response


def get_ad(ad_id: int, session: Session) -> Ad:
    ad = session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, 'Ad not found')
    return ad


class AdView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'creation_time': int(ad.creation_time.timestamp()),
                'user': ad.user
            })


    def post(self):
        with Session() as session:
            new_ad = Ad(**request.json)
            try:
                session.add(new_ad)
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'user already exists')
            return jsonify({
                'id': new_ad.id
            })

    def delete(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({
                'status': 'deleted'
            })

app.add_url_rule('/ad/<int:ad_id>/', view_func=AdView.as_view('ad_existed'), methods=['GET', 'DELETE'])
app.add_url_rule('/ad/', view_func=AdView.as_view('ad_new'), methods=['POST'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)