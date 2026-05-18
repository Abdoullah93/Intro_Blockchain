#!/usr/bin/env python3
"""
TP 3 — Cryptographie appliquée : Code de démarrage
====================================================
EPSI Auxerre — Blockchain M1 — 19 mai 2026

Prérequis : pip install ecdsa
Complétez les parties # TODO dans l'ordre numérique.
"""

import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError


# ============================================================
# PARTIE 1 : Génération des clés
# ============================================================

def generate_keypair():
    """
    Génère une paire de clés ECDSA sur la courbe SECP256k1.
    (La même courbe utilisée par Bitcoin et Ethereum)

    Returns:
        (private_key, public_key) -- tuple (SigningKey, VerifyingKey)
    """
    # TODO 1 : Générer une clé privée avec SigningKey.generate(curve=SECP256k1)
    #          En déduire la clé publique avec private_key.get_verifying_key()
    #          Retourner le tuple (private_key, public_key)
    pass


# ============================================================
# PARTIE 2 : Signature d'une transaction
# ============================================================

def sign_transaction(private_key, transaction: str) -> bytes:
    """
    Signe une transaction avec la clé privée.

    Args:
        private_key  -- objet SigningKey (clé privée d'Alice)
        transaction  -- chaîne texte décrivant la transaction

    Returns:
        signature (bytes) -- la signature numérique
    """
    # TODO 2 :
    # 1. Encoder la transaction : transaction.encode()
    # 2. Signer avec : private_key.sign(message_bytes)
    # 3. Retourner la signature (bytes)
    pass


# ============================================================
# PARTIE 3 : Vérification de la signature
# ============================================================

def verify_transaction(public_key, transaction: str, signature: bytes) -> bool:
    """
    Vérifie qu'une signature est valide pour une transaction donnée.

    Args:
        public_key  -- objet VerifyingKey (clé publique de l'expéditeur)
        transaction -- la transaction dont on vérifie la signature
        signature   -- les bytes de la signature

    Returns:
        True si valide, False sinon.
    """
    # TODO 3 :
    # Utiliser : public_key.verify(signature, transaction.encode())
    # Cette méthode lève BadSignatureError si invalide.
    # Capturer l'exception et retourner False dans ce cas.
    # Retourner True si aucune exception n'est levée.
    pass


# ============================================================
# PARTIE 4 : Dérivation d'adresse de portefeuille
# ============================================================

def derive_address(public_key) -> str:
    """
    Dérive une adresse de portefeuille depuis la clé publique.

    Implémentation simplifiée (sans Base58Check) :
      adresse = SHA-256(SHA-256(clé_publique_bytes)).hexdigest()[:40]

    Args:
        public_key -- objet VerifyingKey

    Returns:
        adresse (str) -- 40 caractères hexadécimaux
    """
    # TODO 4 :
    # 1. Extraire les bytes : public_key.to_string()
    # 2. Premier hash SHA-256 (utiliser .digest() pour obtenir des bytes)
    # 3. Deuxième hash SHA-256 sur le résultat (utiliser .hexdigest())
    # 4. Retourner les 40 premiers caractères
    pass


# ============================================================
# PARTIE 5 : Portefeuille simplifié
# ============================================================

class Wallet:
    """
    Portefeuille avec clé privée, clé publique et adresse.
    """
    def __init__(self, name: str):
        self.name = name
        # TODO 5 : Appeler generate_keypair() et stocker private_key / public_key
        #          Dériver l'adresse avec derive_address()
        self.private_key = None
        self.public_key  = None
        self.address     = None

    def __repr__(self):
        addr = self.address[:16] + "..." if self.address else "N/A"
        return f"Wallet({self.name}, address={addr})"


# ============================================================
# MAIN : Simulation complète
# ============================================================

if __name__ == "__main__":
    print("=" * 65)
    print("TP3 — Cryptographie appliquée à la Blockchain")
    print("=" * 65)

    # Création de deux portefeuilles
    alice = Wallet("Alice")
    bob   = Wallet("Bob")

    print(f"\nAlice : {alice}")
    print(f"Bob   : {bob}")

    # Transaction d'Alice vers Bob
    transaction = "Alice -> Bob : 5 BTC"
    print(f"\nTransaction : '{transaction}'")

    # Signature par Alice
    signature = sign_transaction(alice.private_key, transaction)
    if signature:
        print(f"Signature (64 premiers hex) : {signature.hex()[:64]}...")

    # Vérification normale
    result = verify_transaction(alice.public_key, transaction, signature)
    print(f"\nVérification avec clé ALICE : {result}")  # Attendu : True

    # TODO 6 — Exercice 3 : Tentative de fraude
    # Décommentez et complétez :
    # result_fraud = verify_transaction(bob.public_key, transaction, signature)
    # print(f"Vérification avec clé BOB (fraude) : {result_fraud}")  # Attendu : False

    # Modifiez la transaction et revérifiez :
    # transaction_falsifiee = "Alice -> Mallory : 5 BTC"
    # result_tamper = verify_transaction(alice.public_key, transaction_falsifiee, signature)
    # print(f"Vérification message falsifié : {result_tamper}")  # Attendu : False

    # Affichage des tailles
    if alice.private_key and alice.public_key and signature:
        print("\n--- Tailles des données ---")
        print(f"Clé privée      : {len(alice.private_key.to_string())} bytes")
        print(f"Clé publique    : {len(alice.public_key.to_string())} bytes")
        print(f"Signature       : {len(signature)} bytes")
        print(f"Adresse (hex)   : {len(alice.address) if alice.address else 'N/A'} caractères")
