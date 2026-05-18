#!/usr/bin/env python3
"""
TP 4 — Blockchain P2P avec Flask : Code de démarrage
=====================================================
EPSI Auxerre — Blockchain M1 — 19 mai 2026

Prérequis : pip install flask requests
Lancement : python tp4_node_starter.py --port 5000

Complétez les parties # TODO dans l'ordre numérique.
"""

import hashlib
import time
import json
import argparse
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# ============================================================
# ÉTAT GLOBAL DU NŒUD
# ============================================================

blockchain = []     # Liste de blocs (dicts)
mempool    = []     # Transactions en attente de minage
peers      = set()  # Ensemble des URL des nœuds pairs

DIFFICULTY = 3      # Nombre de zéros hexadécimaux requis en tête du hash


# ============================================================
# FONCTIONS DE BASE
# ============================================================

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    """
    Calcule le SHA-256 d'un bloc à partir de ses champs.
    IMPORTANT : json.dumps avec sort_keys=True assure la reproductibilité.
    """
    content = f"{index}{previous_hash}{timestamp}{json.dumps(data, sort_keys=True)}{nonce}"
    return hashlib.sha256(content.encode()).hexdigest()


def create_block(data, previous_hash):
    """
    Crée et mine un nouveau bloc.

    Args:
        data          -- liste de transactions (ou ["Genesis Block"])
        previous_hash -- hash du bloc précédent

    Returns:
        dict représentant le bloc avec les champs :
        index, timestamp, data, previous_hash, nonce, hash
    """
    # TODO 1 : Implémenter la création et le minage
    # Algorithme :
    #   index     = len(blockchain)
    #   timestamp = time.time()
    #   nonce     = 0
    #   prefix    = "0" * DIFFICULTY
    #   Calculer hash_val = calculate_hash(index, previous_hash, timestamp, data, nonce)
    #   Boucle : tant que hash_val ne commence pas par prefix :
    #       nonce += 1
    #       hash_val = calculate_hash(...)
    #   Retourner le dict du bloc avec tous les champs
    pass


def create_genesis_block():
    """Crée le bloc de genèse (index=0, previous_hash='0' * 64)."""
    return create_block(["Genesis Block"], "0" * 64)


# ============================================================
# ROUTES API REST
# ============================================================

@app.route('/chain', methods=['GET'])
def get_chain():
    """Retourne la blockchain complète en JSON."""
    return jsonify({
        'chain' : blockchain,
        'length': len(blockchain)
    }), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Ajoute une nouvelle transaction au mempool."""
    body = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in body for k in required):
        return jsonify({'error': 'Champs manquants : sender, recipient, amount'}), 400

    # TODO 2 : Ajouter la transaction au mempool
    # Créer un dict {'sender': ..., 'recipient': ..., 'amount': ...}
    # L'ajouter à mempool
    # Retourner un message de succès avec code 201
    pass


@app.route('/mine', methods=['GET'])
def mine():
    """Mine un nouveau bloc avec les transactions du mempool."""
    # TODO 3 : Implémenter le minage
    # Étapes :
    #   1. Vérifier que mempool n'est pas vide → 400 si vide
    #   2. last_hash = blockchain[-1]['hash']
    #   3. new_block = create_block(mempool.copy(), last_hash)
    #   4. mempool.clear()
    #   5. blockchain.append(new_block)
    #   6. broadcast_block(new_block)  # propagation aux pairs
    #   7. Retourner les infos du bloc avec code 200
    pass


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """Enregistre une liste de nœuds pairs (par URL)."""
    body = request.get_json()
    nodes_list = body.get('nodes', [])
    if not nodes_list:
        return jsonify({'error': 'Fournir une liste de nœuds'}), 400

    # TODO 4 : Ajouter chaque URL dans peers (sans trailing slash)
    # Astuce : node_url.rstrip('/')
    # Retourner la liste des pairs et un message de succès (201)
    pass


@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflicts():
    """
    Exécute l'algorithme de consensus.
    Remplace la chaîne locale par la plus longue chaîne valide trouvée.
    """
    replaced = consensus()
    if replaced:
        return jsonify({'message': 'Chaîne remplacée par une plus longue', 'new_chain': blockchain}), 200
    return jsonify({'message': 'La chaîne locale est déjà la plus longue', 'chain': blockchain}), 200


@app.route('/blocks/receive', methods=['POST'])
def receive_block():
    """
    Reçoit un bloc propagé par un pair et l'ajoute si valide.
    """
    block = request.get_json()
    last  = blockchain[-1]
    prefix = "0" * DIFFICULTY

    # TODO 6 : Valider et traiter le bloc reçu
    # Cas 1 : block['index'] == len(blockchain) (bloc suivant attendu)
    #   → Vérifier : previous_hash, hash starts with prefix, hash == calculate_hash(...)
    #   → Si OK : blockchain.append(block), retourner 200
    #   → Sinon : retourner 409 (conflit)
    # Cas 2 : block['index'] > len(blockchain) (on est en retard)
    #   → Appeler consensus() pour se rattraper
    #   → Retourner 200
    # Cas 3 : bloc déjà connu ou fork inférieur → retourner 200 (ignorer)
    pass


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def broadcast_block(block):
    """
    Propage un bloc nouvellement miné à tous les nœuds pairs.
    Les erreurs de connexion sont ignorées (nœud hors ligne).
    """
    for peer in peers:
        try:
            requests.post(f"{peer}/blocks/receive", json=block, timeout=3)
            print(f"  [BROADCAST] Bloc {block['index']} envoyé à {peer}")
        except requests.exceptions.ConnectionError:
            print(f"  [WARN] Pair inaccessible : {peer}")


def consensus():
    """
    Règle de la chaîne la plus longue (Nakamoto Consensus).

    Parcourt tous les pairs, récupère leur chaîne,
    adopte la plus longue si elle est valide et plus longue que la nôtre.

    Returns:
        True si la chaîne locale a été remplacée, False sinon.
    """
    global blockchain

    # TODO 7 : Implémenter le consensus
    # Pour chaque peer dans peers :
    #   Appeler GET {peer}/chain
    #   Récupérer chain = data['chain'] et length = data['length']
    #   Si length > best_length ET is_valid_chain(chain) :
    #       best_length = length
    #       best_chain  = chain
    # Si une meilleure chaîne est trouvée : blockchain = best_chain, retourner True
    # Sinon retourner False
    pass


def is_valid_chain(chain):
    """
    Valide une blockchain complète.

    Pour chaque bloc i >= 1, vérifie :
      1. chain[i]['previous_hash'] == chain[i-1]['hash']
      2. chain[i]['hash'] == calculate_hash(...)
      3. chain[i]['hash'].startswith("0" * DIFFICULTY)

    Returns:
        True si valide, False sinon.
    """
    # TODO 8 : Implémenter la validation
    pass


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nœud Blockchain P2P')
    parser.add_argument('--port', type=int, default=5000,
                        help='Port d\'écoute du nœud (défaut: 5000)')
    args = parser.parse_args()

    # Initialisation avec le bloc de genèse
    genesis = create_genesis_block()
    if genesis:
        blockchain.append(genesis)
        print(f"[INIT] Bloc de genèse : hash={genesis['hash'][:20]}...")
    else:
        print("[ERREUR] create_genesis_block() retourne None — implémentez le TODO 1 !")

    print(f"[INFO] Nœud démarré sur http://localhost:{args.port}")
    print(f"[INFO] Difficulté PoW : {DIFFICULTY} zéro(s)")
    print(f"[INFO] Routes disponibles :")
    print(f"        GET  /chain")
    print(f"        POST /transactions/new")
    print(f"        GET  /mine")
    print(f"        POST /nodes/register")
    print(f"        GET  /nodes/resolve")
    print(f"        POST /blocks/receive")

    app.run(host='0.0.0.0', port=args.port, debug=False)
