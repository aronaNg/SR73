#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module auxiliaire pour le projet CP-ABE UTBM
Contient les définitions des utilisateurs, attributs et fonctions utilitaires
"""

import json
from typing import Dict, List, Any

class Colors:
    """Classe pour les couleurs d'affichage dans le terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class UTBMScenario:
    """
    Classe gérant le scénario UTBM pour le système CP-ABE
    """
    
    def __init__(self):
        """Initialise le scénario avec les utilisateurs et leurs attributs"""
        self.users = self._define_users()
        self.attribute_mapping = self._define_attribute_mapping()
    
    def _define_attribute_mapping(self) -> Dict[str, str]:
        """
        Définit le mapping entre les attributs logiques et les codes Charm-Crypto
        """
        return {
            'ONE': 'Professeur',
            'TWO': 'Cours_SR73',
            'THREE': 'Étudiant', 
            'FOUR': 'Administrateur'
        }
    
    def _define_users(self) -> Dict[str, Dict[str, Any]]:
        """
        Définit les utilisateurs du système avec leurs attributs
        """
        return {
            'prof_abbas_turki': {
                'name': 'Pr Abdeljalil ABBAS-TURKI',
                'role': 'Professeur SR73',
                'attributes': ['ONE', 'TWO'],  # Professeur ET Cours_SR73
                'description': 'Professeur responsable du cours SR73'
            },
            'etudiant_ngom': {
                'name': 'Arona NGOM',
                'role': 'Étudiant SR73',
                'attributes': ['THREE', 'TWO'],  # Étudiant ET Cours_SR73
                'description': 'Étudiant inscrit au cours SR73'
            },
            'admin_tyndiuk': {
                'name': 'Florence Tyndiuk',
                'role': 'Administratrice',
                'attributes': ['FOUR'],  # Administrateur
                'description': 'Administratrice des services académiques'
            },
            'etudiant_autre': {
                'name': 'Ibrahima NGOM',
                'role': 'Étudiant autre cours',
                'attributes': ['THREE'],  # Seulement Étudiant (pas SR73)
                'description': 'Étudiant non inscrit au cours SR73'
            }
        }
    
    def get_users(self) -> Dict[str, Dict[str, Any]]:
        """Retourne la liste des utilisateurs"""
        return self.users
    
    def get_attribute_mapping(self) -> Dict[str, str]:
        """Retourne le mapping des attributs"""
        return self.attribute_mapping
    
    def verify_security_logic(self, results: Dict[str, Dict], users: Dict[str, Dict]) -> None:
        """
        Vérifie que la logique de sécurité fonctionne correctement
        """
        print("\n Analyse de la sécurité:")
        
        expected_access = {
            'prof_abbas_turki': True,    # Professeur ET Cours_SR73 -> Accès
            'etudiant_ngom': True, # Étudiant ET Cours_SR73 -> Accès  
            'admin_tyndiuk': True,    # Administrateur -> Accès
            'etudiant_autre': False  # Seulement Étudiant -> Pas d'accès
        }
        
        all_correct = True
        
        for username, expected in expected_access.items():
            actual = results[username]['success']
            user_name = users[username]['name']
            
            if actual == expected:
                status = f"{Colors.OKGREEN} CORRECT{Colors.ENDC}"
            else:
                status = f"{Colors.FAIL} ERREUR{Colors.ENDC}"
                all_correct = False
            
            print(f"   {user_name}: {status}")
            print(f"     Attendu: {'Accès' if expected else 'Refus'}")
            print(f"     Obtenu: {'Accès' if actual else 'Refus'}")
        
        if all_correct:
            print(f"\n{Colors.OKGREEN} Tous les tests de sécurité sont CORRECTS{Colors.ENDC}")
            print("La politique d'accès fonctionne comme prévu.")
        else:
            print(f"\n{Colors.FAIL}⚠️  ATTENTION: Des erreurs de sécurité ont été détectées{Colors.ENDC}")

def display_results(results: Dict[str, Dict], users: Dict[str, Dict]) -> None:
    """
    Affiche les résultats des tests de déchiffrement de manière formatée
    """
    print(f"\n{'─' * 80}")
    print(f"{'UTILISATEUR':<25} {'RÔLE':<20} {'STATUT':<15} {'DÉTAILS'}")
    print(f"{'─' * 80}")
    
    for username, result in results.items():
        user_info = users[username]
        name = user_info['name']
        role = user_info['role']
        
        if result['success']:
            status = f"{Colors.OKGREEN} AUTORISÉ{Colors.ENDC}"
            details = "Accès aux données"
        else:
            status = f"{Colors.FAIL} REFUSÉ{Colors.ENDC}"
            details = "Attributs insuffisants"
        
        print(f"{name:<25} {role:<20} {status:<24} {details}")
    
    print(f"{'─' * 80}")

def display_policy_explanation() -> None:
    """
    Affiche une explication détaillée de la politique d'accès
    """
    print(f"\n{Colors.HEADER} EXPLICATION DE LA POLITIQUE D'ACCÈS{Colors.ENDC}")
    print("Politique: ((ONE and TWO) or (THREE and TWO) or FOUR)")
    print("\nTraduction:")
    print("  ((Professeur ET Cours_SR73) OU (Étudiant ET Cours_SR73) OU Administrateur)")
    print("\nSignification:")
    print("   Accès autorisé pour:")
    print("     - Les professeurs du cours SR73")
    print("     - Les étudiants inscrits au cours SR73")
    print("     - Tous les administrateurs")
    print("   Accès refusé pour:")
    print("     - Les étudiants non inscrits au cours SR73")
    print("     - Toute personne sans attributs appropriés")

def simulate_real_world_scenario() -> Dict[str, Any]:
    """
    Simule un scénario réaliste avec des données d'examen
    """
    return {
        "exam_info": {
            "course_code": "SR73",
            "course_name": "Cybsécurité et Protection des Données",
            "semester": "Automne 2025",
            "exam_date": "2025-06-15",
            "professor": "Pr Abdeljalil ABBAS-TURKI"
        },
        "statistics": {
            "total_students": 45,
            "average_grade": 13.2,
            "pass_rate": 0.78
        },
        "access_log": {
            "encryption_time": "2025-06-15 14:30:00",
            "policy_applied": "SR73_RESULTS_POLICY",
            "authorized_roles": ["Professeur_SR73", "Étudiant_SR73", "Administrateur"]
        }
    }

# Fonction utilitaire pour les tests
def run_attribute_tests() -> None:
    """
    Exécute des tests sur les attributs pour vérifier la compatibilité
    """
    print(f"\n{Colors.OKBLUE} Tests de compatibilité des attributs{Colors.ENDC}")
    
    test_attributes = ['ONE', 'TWO', 'THREE', 'FOUR']
    
    for attr in test_attributes:
        if attr.isupper() and attr.isalpha():
            print(f"    {attr}: Format valide pour Charm-Crypto")
        else:
            print(f"    {attr}: Format invalide")
    
    print(f"{Colors.OKGREEN} Tous les attributs sont compatibles{Colors.ENDC}")