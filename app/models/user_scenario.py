from django.db import models
from django.contrib.auth.models import User
from app.models.scenario_config import ScenarioConfig
from app.models.template_scenario_model import TemplateScenario

from app.models.team import Team


class ScenarioState(models.Model):
    counter = models.IntegerField()
    cost = models.FloatField()
    day = models.IntegerField()


class UserScenario(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    config = models.ForeignKey(
        ScenarioConfig, on_delete=models.SET_NULL, null=True, blank=True
    )
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.OneToOneField(
        ScenarioState, on_delete=models.SET_NULL, null=True, blank=True
    )
    model = models.CharField(max_length=8, null=True, blank=True)
    template = models.ForeignKey(TemplateScenario, on_delete=models.SET_NULL, null=True)