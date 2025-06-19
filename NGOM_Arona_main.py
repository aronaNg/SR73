#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet CP-ABE UTBM - Protection des résultats d'examens
Scénario : Un professeur chiffre des résultats d'examens avec une politique d'accès
permettant aux étudiants concernés et aux administrateurs d'y accéder.
"""

from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from NGOM_Arona_util import UTBMScenario, display_results, Colors
import json

def main():
    """
    Fonction principale implémentant le scénario CP-ABE UTBM
    """
    print(f"{Colors.HEADER}{'='*60}")
    print(" SYSTÈME DE PROTECTION DES RÉSULTATS D'EXAMENS - UTBM")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    # Initialisation du système cryptographique
    print(f"{Colors.OKBLUE} Étape 1: Initialisation du système ABE{Colors.ENDC}")
    group = PairingGroup('SS512')
    cpabe = CPabe_BSW07(group)
    hyb_abe = HybridABEnc(cpabe, group)
    
    # Génération des paramètres publics et de la clé maître
    (pk, mk) = hyb_abe.setup()
    print(f"{Colors.OKGREEN} Système ABE initialisé avec succès{Colors.ENDC}\n")
    
    # Création du scénario UTBM
    scenario = UTBMScenario()
    
    # Définition des données sensibles (résultats d'examens)
    exam_results = {
        "course": "SR73 - Cybsécurité et Protection des Données",
        "semester": "A25",
        "results": [
            {"student_id": "21804567", "name": "Arona NGOM", "grade": 15.5},
            {"student_id": "21805432", "name": "Stan HOFFMANN", "grade": 14.0},
            {"student_id": "21806789", "name": "Michel DIENG", "grade": 14.5}
        ],
        "professor": "Pr Abdeljalil ABBAS-TURKI",
        "date": "2025-06-15"
    }
    
    # Conversion en JSON pour le chiffrement
    message = json.dumps(exam_results, indent=2, ensure_ascii=False)
    
    print(f"{Colors.OKBLUE} Étape 2: Définition de la politique d'accès{Colors.ENDC}")
    # Politique d'accès : (Professeur ET Cours_SR73) OU (Étudiant ET Cours_SR73) OU Administrateur
    access_policy = '((ONE and TWO) or (THREE and TWO) or FOUR)'
    
    print(f" Politique d'accès définie: {access_policy}")
    print(f"   - ONE: Professeur")
    print(f"   - TWO: Cours_SR73") 
    print(f"   - THREE: Étudiant")
    print(f"   - FOUR: Administrateur")
    print(f"{Colors.OKGREEN} Politique d'accès configurée{Colors.ENDC}\n")
    
    print(f"{Colors.OKBLUE} Étape 3: Chiffrement des données{Colors.ENDC}")
    # Chiffrement du message avec la politique d'accès
    ciphertext = hyb_abe.encrypt(pk, message, access_policy)
    print(f"{Colors.OKGREEN} Résultats d'examens chiffrés avec succès{Colors.ENDC}")
    print(f" Données chiffrées: {len(str(ciphertext))} caractères\n")
    
    print(f"{Colors.OKBLUE} Étape 4: Génération des clés utilisateurs{Colors.ENDC}")
    
    # Génération des clés pour différents utilisateurs
    users = scenario.get_users()
    user_keys = {}
    
    for username, user_info in users.items():
        attributes = user_info["attributes"]
        user_keys[username] = hyb_abe.keygen(pk, mk, attributes)
        print(f" Clé générée pour {user_info['name']}")
        print(f"   Attributs: {', '.join(attributes)}")
    
    print(f"{Colors.OKGREEN} Toutes les clés utilisateurs générées{Colors.ENDC}\n")
    
    print(f"{Colors.OKBLUE} Étape 5: Tests de déchiffrement{Colors.ENDC}")
    
    # Test de déchiffrement pour chaque utilisateur
    results = {}
    
    for username, user_info in users.items():
        print(f"\n Test de déchiffrement pour {user_info['name']} ({user_info['role']}):")
        print(f"   Attributs: {', '.join(user_info['attributes'])}")
        
        try:
            # Tentative de déchiffrement
            decrypted_message = hyb_abe.decrypt(pk, user_keys[username], ciphertext)
            
            if decrypted_message:
                results[username] = {
                    "success": True,
                    "message": "Accès autorisé",
                    "data": json.loads(decrypted_message)
                }
                print(f"   {Colors.OKGREEN} ACCÈS AUTORISÉ{Colors.ENDC}")
            else:
                results[username] = {
                    "success": False,
                    "message": "Accès refusé - attributs insuffisants"
                }
                print(f"   {Colors.FAIL} ACCÈS REFUSÉ{Colors.ENDC}")
                
        except Exception as e:
            results[username] = {
                "success": False,
                "message": f"Erreur de déchiffrement: {str(e)}"
            }
            print(f"   {Colors.FAIL} ERREUR: {str(e)}{Colors.ENDC}")
    
    # Affichage des résultats finaux
    print(f"\n{Colors.HEADER} RÉSUMÉ DES TESTS D'ACCÈS{Colors.ENDC}")
    display_results(results, users)
    
    # Vérification de la logique de sécurité
    print(f"\n{Colors.HEADER} VÉRIFICATION DE LA SÉCURITÉ{Colors.ENDC}")
    scenario.verify_security_logic(results, users)
    
    print(f"\n{Colors.HEADER} SCÉNARIO COMPLÉTÉ AVEC SUCCÈS{Colors.ENDC}")
    print("Le système CP-ABE protège efficacement les données sensibles")
    print("selon les politiques d'accès définies par l'UTBM.")

if __name__ == "__main__":
    main()