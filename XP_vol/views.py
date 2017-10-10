from . import models
from ._builtin import Page, WaitPage
#from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Instructions(Page):
    pass


class SlidersTask(Page):
    form_model = models.Player
    form_fields = ['numberOfTasksDone']

    def var_for_tempalte(self):
        return{
            'type_joueur_': self.player.type_joueur
        }

    def before_next_page(self):
        self.player.payoff += 1250


class WaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Recapitulatif(Page):
    pass


class Phase_vote(Page):
    def is_displayed(self):
        return (self.player.is_chosen == 1)

    def vars_for_template(self):
        return {
            'voleur': self.player.is_chosen == 0,
            'voteur': self.player.is_chosen == 1,
        }
    form_model = models.Player
    form_fields = ['vote_sanction']


class ResultsWaitPage_vote_1(WaitPage):
    def after_all_players_arrive(self):
        self.group.choix_des_voteurs()


class ResultsWaitPage_vote_2(WaitPage):
    wait_for_all_groups = True


class Results_vote(Page):

    def vars_for_template(self):
        return {
            'choix_1': self.session.vars['choix_criminels'] == 'choix 1',
        }


class Choix_voleur(Page):
    def is_displayed(self):
        return (self.player.is_chosen == 0)
    form_model = models.Player
    form_fields = ['voler_35','voler_10']

    def vars_for_template(self):
        return {
            'voleur_type_A': self.player.type_voleur == 'A',
        }


class ResultsWaitPage_vol(WaitPage):
    def is_displayed(self):
        return (self.player.is_chosen == 0)

    def after_all_players_arrive(self):
        self.group.interaction_voleurs()
        self.group.Sanctions()


class Expurgement(Page):
    def is_displayed(self):
        return (self.player.vol_realisation == 'voler')
    form_model = models.Player
    form_fields = ['expurgement']


class Rappel_vote(Page):
    def vars_for_template(self):
        return{
            'resultat_vote': self.group.choix_vote
                }

class Choix_voleur_2(Page):
    def is_displayed(self):
        return (self.player.is_chosen == 0)
    form_model = models.Player
    form_fields = ['voler_35_2','voler_10_2']

    def vars_for_template(self):
        return {
            'voleur_type_A': self.player.type_voleur == 'A',
        }

class ResultsWaitPage_vol_2(WaitPage):
    def is_displayed(self):
        return (self.player.is_chosen == 0)

    def after_all_players_arrive(self):
        self.group.interaction_voleurs_2()
        self.group.Sanctions_2()

class Rappel_decisions(Page):
    def vars_for_template(self):
        return{
            'voleur': self.player.is_chosen == 0,
            'voteur': self.player.is_chosen == 1,
            'voleur_type_A': self.player.type_voleur == 'A',
            'decisions_vol_1': self.player.vol_realisation,
            'decisions_vol_2': self.player.vol_realisation_2,
            'vol_1': self.player.vol_realisation == 'voler',
            'vol_2': self.player.vol_realisation_2 == 'voler',
            'detect__1': self.player.vol_detect == 1,
            'detect__2': self.player.vol_detect_2 == 1,
            'expurge': self.player.expurgement,
            'payoff_player': self.player.payoff,
            'vote': self.player.vote_sanction,
            'resultat_vote': self.group.choix_vote
        }

class MerciPage(Page):
    pass

page_sequence = [
    Introduction,
    Instructions,
    SlidersTask,
    WaitPage,
    Recapitulatif,
    Phase_vote,
    ResultsWaitPage_vote_1,
    ResultsWaitPage_vote_2,
    Results_vote,
    Choix_voleur,
    ResultsWaitPage_vol,
    Expurgement,
    #Instructions,
    #SlidersTask,
    #Recapitulatif,
    Rappel_vote,
    Choix_voleur_2,
    ResultsWaitPage_vol_2,
    Rappel_decisions,
    MerciPage

]
