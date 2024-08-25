from __future__ import annotations
from flask import Blueprint, render_template
from flask import jsonify

from ..facade_singleton import FacadeSingleton
# from model.database import inserir_pesquisa, inserir_pergunta, inserir_resposta

main = Blueprint('main', __name__)

@main.route('/api/data', methods=['GET'])
def get_data():
    """
    Endpoint to get all data from the 'database'.
    """
    try:
        facade = FacadeSingleton.get_facade()
        data = facade.get_database()
        return jsonify({'status': 'success', 'result': data}), 200
    except:
        return jsonify({'status': 'error', 'result': {}}), 500
    

@main.route('/api/data/<int:survey_id>', methods=['GET'])
def get_data_by_survey(survey_id):
    """
    Endpoint to get data for a specific survey.
    """
    facade = FacadeSingleton.get_facade()
    data = [entry for entry in facade.get_database() if entry["survey_id"] == survey_id]
    if not data:
        return jsonify({"error": "Survey not found"}), 404
    return jsonify(data), 200
