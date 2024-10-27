from flask import request, jsonify, g
import src.modelos.animal as modelos
from pydantic import ValidationError
import src.repositories.animal as repositories

def criarAnimal():
    dados = request.get_json()
    id_dono = g.user_id
    try:
        animal = modelos.Animal(**dados)
    except ValidationError as e:
        return jsonify({"erro":e.errors()}), 400
    animalDict = animal.model_dump()
    animalId, erro = repositories.criarAnimal(animalDict, id_dono)
    if erro != None:
        return jsonify({"erro": erro}), 500
    return jsonify({"id": animalId}), 201

def buscarAnimais():
    id_dono = g.user_id
    animais, erro = repositories.buscarAnimais(id_dono)
    if erro != None:
        return jsonify({"erro": erro}), 500
    if animais == None:
        return "", 204
    return jsonify(animais), 200

def buscarAnimal(id):
    animal, erro = repositories.buscarAnimal(id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    if animal == None:
        return "", 204
    return jsonify(animal), 200

def editarAnimal(id):
    id_logado = g.user_id
    id_dono, erro = repositories.buscarDono(id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    if id_dono == None:
        return jsonify({"erro": "Nenhum animal com esse id"}), 404
    if id_logado != id_dono:
        return jsonify({"erro": "Você só pode editar seus animais"}), 403
    dados = request.get_json()
    try:
        animal = modelos.Animal(**dados)
    except ValidationError as e:
        return jsonify({"erro":e.errors()}), 400
    animalDict = animal.model_dump()
    _, erro = repositories.editarAnimal(animalDict, id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    return "", 204

def apagarAnimal(id):
    id_logado = g.user_id
    id_dono, erro = repositories.buscarDono(id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    if id_dono == None:
        return jsonify({"erro": "Nenhum animal com esse id"}), 404
    if id_logado != id_dono:
        return jsonify({"erro": "Você só pode apagar seus animais"}), 403
    apagou, erro = repositories.apagarAnimal(id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    if apagou == None:
        return jsonify({"erro": "Nenhum animal com esse id"}), 404
    return jsonify({"id": id}), 200