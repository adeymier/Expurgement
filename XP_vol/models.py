from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random, itertools
import numpy as np


doc = """
Ceci est le jeu de vol et punition de Rustam & Romain (bande d'enculés)
"""


class Constants(BaseConstants):
    name_in_url = 'XP_vol'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def before_session_starts(self):
        players = self.get_players()
        type_voleur = itertools.cycle(['A', 'B'])
        random_3 = random.sample(players, 3)
        for p in players:
            p.numberOfTasksDone = 0
            if p in random_3:
                p.is_chosen = True
                p.type_voleur = ''
                p.type_joueur = 'C'
            else:
                p.is_chosen = False
                p.type_voleur = next(type_voleur)
                p.type_joueur = p.type_voleur

    def creating_session(self):
        players = self.get_players()
        les_voteurs = []
        for p in players:
            if p.is_chosen == True:
                les_voteurs.append(p.id_in_group)
            else:
                pass
        Voleurs_players_A = [p.id_in_group for p in players if p.type_voleur == 'A']
        Voleurs_players_B = [p.id_in_group for p in players if p.type_voleur == 'B']
        group_matrix = [les_voteurs]

        while Voleurs_players_A:
            new_group = [
                Voleurs_players_A.pop(),
                Voleurs_players_B.pop(),
                Voleurs_players_A.pop(),
                Voleurs_players_B.pop(),
            ]
            group_matrix.append(new_group)
        self.set_group_matrix(group_matrix)

        for g in self.get_groups():
            if len(g.get_players()) == 3:
                g.color = "vote"
            else:
                g.color = "pas_vote"


class Group(BaseGroup):
    color = models.CharField()
    choix_vote =  models.CharField()
    def choix_des_voteurs(self):
        if self.color == 'vote':
            votes = [p.vote_sanction for p in self.get_players()]
            choix = list(filter(None, set(votes)))
            resultats = {m: votes.count(m) for m in choix}
            print(resultats)
            if resultats['choix 2'] >= 1:
                self.choix_vote = 'choix 2'
            else:
                self.choix_vote = 'choix 1'
            #ordre = sorted(resultats.items(), key=lambda resultats: resultats[1], reverse=True)
            #self.choix_vote = ordre[0][0]
            self.session.vars['choix_criminels'] = self.choix_vote
        else:
            pass

    def interaction_voleurs(self):
        players = self.get_players()
        for p in players:
            if p.type_voleur == 'A':
                realisation_proba_A = np.random.choice(
                    [450, 125], 1,
                    p=[0.8, 0.2]
                )
                if realisation_proba_A == 450:
                    p.etat_monde_vol = 450
                    p.vol_realisation = p.voler_35
                else:
                    p.etat_monde_vol = 125
                    p.vol_realisation = p.voler_10

            elif p.type_voleur == 'B':
                realisation_proba_B = np.random.choice(
                    [450, 125], 1,
                    p=[0.2, 0.8]
                )
                if realisation_proba_B == 450:
                    p.vol_realisation = p.voler_35
                    p.etat_monde_vol = 450
                else:
                    p.vol_realisation = p.voler_10
                    p.etat_monde_vol = 125

            else:
                pass

        decision = {m.id_in_group: m.vol_realisation for m in players}
        resultat_vol = {m.id_in_group: m.etat_monde_vol for m in players}
        for p in players:
            if p.id_in_group == 1:
                p.matched = 2
                p.decision_matched = decision[2]
                if decision[2] == 'voler':
                    p.payoff -= resultat_vol[2]
                elif decision[2] == 'pas voler':
                    p.payoff += 0
            elif p.id_in_group == 2:
                p.matched = 3
                p.decision_matched = decision[3]
                if decision[3] == 'voler':
                    p.payoff -= resultat_vol[3]
                elif decision[3] == 'pas voler':
                    p.payoff += 0
            elif p.id_in_group == 3:
                p.matched = 4
                p.decision_matched = decision[4]
                if decision[4] == 'voler':
                    p.payoff -= resultat_vol[4]
                elif decision[4] == 'pas voler':
                    p.payoff += 0
            elif p.id_in_group == 4:
                p.matched = 1
                p.decision_matched = decision[1]
                if decision[1] == 'voler':
                    p.payoff -= resultat_vol[1]
                elif decision[1] == 'pas voler':
                    p.payoff += 0

    def Sanctions(self):
        players = self.get_players()
        for p in players:
            p.sanction_informelle = self.session.vars['choix_criminels']
            detect = np.random.choice(
                ['1', '0'], 1,
                p=[0.5, 0.5]
            )
            if detect == ['1']:
                p.vol_detect = 1
                print('detect')
            elif detect == ['0']:
                p.vol_detect = 0
                print('undetect')
            print(p.vol_detect)
            if self.session.vars['choix_criminels'] == 'choix 1':
                p.payoff += 450
                if p.vol_realisation == 'voler' and p.vol_detect == 1:
                    p.payoff += -200
                else:
                    pass

            elif self.session.vars['choix_criminels'] == 'choix 2':
                if p.vol_realisation == 'voler':
                    if p.vol_detect == 1:
                        p.payoff += -200
                        p.payoff += 250
                        p.condition_1 = 0
                    else:
                        p.payoff += 450
                        p.condition_1 =1
                else:
                    p.payoff += 450
                    p.condition_1 = 1


    def interaction_voleurs_2(self):
        players = self.get_players()
        for p in players:
            if p.type_voleur == 'A':
                realisation_proba_A = np.random.choice(
                    [450, 125], 1,
                    p=[0.8, 0.2]
                )
                if realisation_proba_A == 450:
                    p.etat_monde_vol_2 = 450
                    p.vol_realisation_2 = p.voler_35_2
                else:
                    p.etat_monde_vol_2 = 125
                    p.vol_realisation_2 = p.voler_10_2
            elif p.type_voleur == 'B':
                realisation_proba_B = np.random.choice(
                    [450, 125], 1,
                    p=[0.2, 0.8]
                )
                if realisation_proba_B == 450:
                    p.vol_realisation_2 = p.voler_35_2
                    p.etat_monde_vol_2 = 450
                else:
                    p.vol_realisation_2 = p.voler_10_2
                    p.etat_monde_vol_2 = 125
            else:
                pass

        decision_2 = {m.id_in_group: m.vol_realisation for m in players}
        resultat_vol_2 = {m.id_in_group: m.etat_monde_vol for m in players}
        for p in players:
            if p.id_in_group == 1:
                p.matched_2 = 4
                p.decision_matched_2 = decision_2[4]
                if decision_2[4] == 'voler':
                    p.payoff -= resultat_vol_2[4]
                elif decision_2[4] == 'pas voler':
                    p.payoff += 0
            elif p.id_in_group == 2:
                p.matched_2 = 1
                p.decision_matched_2 = decision_2[1]
                if decision_2[1] == 'voler':
                    p.payoff -= resultat_vol_2[1]
                elif decision_2[1] == 'pas voler':
                    p.payoff += 0
            elif p.id_in_group == 3:
                p.matched_2 = 2
                p.decision_matched_2 = decision_2[2]
                if decision_2[2] == 'voler':
                    p.payoff -= resultat_vol_2[2]
                elif decision_2[2] == 'pas voler':
                    p.payoff += 0
            elif p.id_in_group == 4:
                p.matched_2 = 3
                p.decision_matched_2 = decision_2[3]
                if decision_2[3] == 'voler':
                    p.payoff -= resultat_vol_2[3]
                elif decision_2[3] == 'pas voler':
                    p.payoff += 0

    def Sanctions_2(self):
        players = self.get_players()
        for p in players:
            detect_2 = np.random.choice(
                ['1', '0'], 1,
                p=[0.5, 0.5]
            )
            if detect_2 == ['1']:
                p.vol_detect_2 = 1
                print('detect')
            elif detect_2 == ['0']:
                p.vol_detect_2 = 0
                print('undetect')
            print(p.vol_detect_2)
            if self.session.vars['choix_criminels'] == 'choix 1':
                p.payoff += 450
                if p.vol_realisation_2 == 'voler' and p.vol_detect_2 == 1:
                    p.payoff += -200
                else :
                    p.payoff += 450
            elif self.session.vars['choix_criminels'] == 'choix 2':
                if p.vol_realisation_2 == 'voler':
                    if p.vol_detect_2 == 1:
                        p.payoff += 250
                    elif p.vol_detect_2 == '0':
                        if p.condition_1 == 1:
                            p.payoff += 450
                        elif p.expurgement == 'Effacer':
                            p.payoff += 450
                        else:
                            p.payoff +=250
                elif p.vol_realisation_2 == 'pas voler':
                    if p.condition_1 == 1:
                        p.payoff += 450
                    elif p.expurgement == 'Effacer':
                        p.payoff += 450
                    else:
                        p.payoff += 250

class Player(BasePlayer):

    type_joueur = models.CharField()
    numberOfTasksDone = models.IntegerField()
    condition_1 = models.IntegerField(initial=0)
    matched = models.CharField()
    decision_matched = models.CharField()
    etat_monde_vol = models.IntegerField()
    vol_realisation = models.CharField()
    vol_detect = models.IntegerField()
    sanction_informelle = models.CharField()

    matched_2 = models.CharField()
    decision_matched_2 = models.CharField()
    etat_monde_vol_2 = models.IntegerField()
    vol_realisation_2 = models.CharField()
    vol_detect_2 = models.IntegerField()

    expurgement = models.CharField(
        choices=['Effacer', 'Pas Effacer'],
        verbose_name='Choisissez l option que vous souhaitez',
        widget=widgets.RadioSelect()
    )
    vote_sanction = models.CharField(
        choices=['choix 1','choix 2'],
        verbose_name='Choisissez l option qui vous convient le plus',
        widget=widgets.RadioSelect()
    )
    voler_35 = models.CharField(
        choices=['voler', 'pas voler'],
        verbose_name='Choisissez si vous volez ou pas',
        widget=widgets.RadioSelect()
    )
    voler_10 = models.CharField(
        choices=['voler', 'pas voler'],
        verbose_name='Choisissez si vous volez ou pas',
        widget=widgets.RadioSelect()
    )
    voler_35_2 = models.CharField(
        choices=['voler', 'pas voler'],
        verbose_name='Choisissez si vous volez ou pas',
        widget=widgets.RadioSelect()
    )
    voler_10_2 = models.CharField(
        choices=['voler', 'pas voler'],
        verbose_name='Choisissez si vous volez ou pas',
        widget=widgets.RadioSelect()
    )
    is_chosen = models.BooleanField()
    type_voleur = models.CharField()
    def role(self):
        if self.is_chosen == 1:
            return 'voteur'
        if self.is_chosen == 0:
            return 'voleur'