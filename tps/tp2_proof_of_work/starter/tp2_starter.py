#!/usr/bin/env python3
"""
TP 2 — Proof of Work : Code de démarrage
=========================================
EPSI Auxerre — Blockchain M1 — 19 mai 2026

Complétez les parties marquées # TODO dans l'ordre numérique.
"""

import hashlib
import time

# ============================================================
# PARTIE 1 : Structure d'un Bloc
# ============================================================

class Block:
    """
    Représente un bloc dans la blockchain.

    Attributs :
        index         -- position du bloc dans la chaîne
        previous_hash -- hash du bloc précédent (maillon)
        timestamp     -- horodatage de création
        data          -- données/transactions du bloc
        nonce         -- nombre d'essais pour le PoW
        hash          -- empreinte cryptographique du bloc
    """

    def __init__(self, index, previous_hash, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.data = data
        self.nonce = 0
        # TODO 1 : Calculer le hash initial du bloc
        # Remplacez la ligne ci-dessous par l'appel à calculate_hash()
        self.hash = None

    def calculate_hash(self):
        """
        Calcule le SHA-256 du contenu du bloc.
        La chaîne à hacher combine index, previous_hash,
        timestamp, data et nonce (tous convertis en str).
        """
        # TODO 2 : Construire la chaîne et retourner son SHA-256
        # Astuce : content = str(self.index) + self.previous_hash + ...
        # Retourner : hashlib.sha256(content.encode()).hexdigest()
        pass

    def __repr__(self):
        hash_str = self.hash[:12] + "..." if self.hash else "None"
        return (f"Block(index={self.index}, nonce={self.nonce}, "
                f"hash={hash_str})")


# ============================================================
# PARTIE 2 : Proof of Work
# ============================================================

def mine_block(block, difficulty=4):
    """
    Effectue la Preuve de Travail sur un bloc.

    Incrémente block.nonce jusqu'à ce que block.hash
    commence par 'difficulty' zéros hexadécimaux.

    Args:
        block      -- le bloc à miner (modifié en place)
        difficulty -- nombre de zéros requis en tête du hash

    Returns:
        Le bloc avec nonce et hash mis à jour.
    """
    prefix = "0" * difficulty

    # TODO 3 : Implémenter la boucle de minage
    # Rappel : la condition est block.hash.startswith(prefix)
    # Tant que la condition n'est PAS satisfaite :
    #   block.nonce += 1
    #   block.hash = block.calculate_hash()
    # Retourner le bloc miné
    pass


# ============================================================
# PARTIE 3 : La Blockchain
# ============================================================

class Blockchain:
    """Gère une liste chaînée de blocs avec Proof of Work."""

    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.chain = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Crée et mine le premier bloc (index=0, previous_hash='000...0')."""
        genesis = Block(0, "0" * 64, "Genesis Block")
        # TODO 4 : Miner le bloc de genèse avec self.difficulty
        #          puis l'ajouter à self.chain
        pass

    def get_last_block(self):
        """Retourne le dernier bloc de la chaîne."""
        return self.chain[-1]

    def add_block(self, data):
        """
        Crée un nouveau bloc, le mine et l'ajoute à la chaîne.

        Args:
            data -- les données du nouveau bloc

        Returns:
            Le temps de minage en secondes (float).
        """
        # TODO 5 :
        # 1. Récupérer le dernier bloc avec get_last_block()
        # 2. Créer un nouveau Block(index, last.hash, data)
        # 3. Mesurer le temps de minage (time.time())
        # 4. Miner le bloc avec mine_block(...)
        # 5. Ajouter le bloc à self.chain
        # 6. Retourner le temps écoulé
        pass

    def is_valid(self):
        """
        Vérifie l'intégrité complète de la blockchain.

        Pour chaque bloc (i >= 1), vérifier :
          1. current.hash == current.calculate_hash()  (données non altérées)
          2. current.previous_hash == previous.hash    (chaînage correct)
          3. current.hash.startswith("0" * difficulty) (PoW respecté)

        Afficher un message d'erreur pour chaque violation.
        Retourner True si tout est valide, False sinon.
        """
        # TODO 6 : Implémenter la validation complète
        pass


# ============================================================
# PARTIE 4 : Expérimentation
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TP2 — Proof of Work : Expérimentation")
    print("=" * 60)

    # --- Test des difficultés ---
    print("\n[1] Test de minage avec différentes difficultés :\n")

    for difficulty in [1, 2, 3, 4]:
        bc = Blockchain(difficulty=difficulty)
        start = time.time()
        bc.add_block("Transaction: Alice -> Bob : 10 BTC")
        duration = time.time() - start

        last = bc.get_last_block()
        print(f"  Difficulté {difficulty} | Nonce = {last.nonce:>8} | "
              f"Hash = {last.hash[:20] if last.hash else 'N/A'}... | "
              f"Temps = {duration:.4f}s")

    # --- Validation ---
    print("\n[2] Validation de la chaîne :\n")
    bc = Blockchain(difficulty=3)
    bc.add_block("Alice -> Bob : 5 BTC")
    bc.add_block("Bob -> Charlie : 2 BTC")
    print("  Résultat is_valid() :", bc.is_valid())

    # --- TODO 7 (Bonus) : Falsification ---
    # Décommentez et complétez les lignes suivantes pour tester la falsification :
    # print("\n[3] Tentative de falsification :\n")
    # bc.chain[1].data = "Alice -> Mallory : 50 BTC"
    # Recalculez le hash du bloc 1 (sans refaire le PoW) :
    # bc.chain[1].hash = bc.chain[1].calculate_hash()
    # print("  Résultat après falsification :", bc.is_valid())
    # Que constatez-vous ? Pourquoi is_valid() retourne-t-il False ?
