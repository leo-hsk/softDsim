from typing import Optional

from bson.objectid import ObjectId

from app.src.dataObjects import WorkPackage
from app.src.decision_tree import ActionList, Decision, SimulationDecision
from app.src.team import Team, ScrumTeam
from app.src.task_queue import TaskQueue
from app.src.scorecard import ScoreCard
from utils import month_to_day, remove_none_values, YAMLReader

# Config Variables
STRESS_ERROR_INCREASE = YAMLReader.read('stress', 'error')



class Scenario:
    """
    A Scenario is a predefined 'Story' that users go through. When a user starts a scenario, a UserScenario is created.
    """
    def __init__(self, name: str = "Unnamed Scenario",
                budget: int = 0,
                scheduled_days: int = 0,
                decisions: list = None,
                desc: str = "",
                tasks_easy: int = 0,
                tasks_medium: int = 0,
                tasks_hard: int = 0,
                pred_c: float = 0.1, 
                _id: ObjectId = None,
                id: ObjectId = None,
                scorecard: ScoreCard = None,
                **kwargs) -> None:
        if id and not _id:
            _id = id
        if decisions is None:
            decisions = []
        self.name = name
        self.budget= budget
        self.scheduled_days=scheduled_days
        self.decisions=decisions
        self.desc=desc
        self.tasks_easy=tasks_easy
        self.tasks_medium=tasks_medium
        self.tasks_hard=tasks_hard
        self.pred_c=pred_c
        self.id = ObjectId() if _id is None else ObjectId(_id)
        self.scorecard = scorecard if isinstance(scorecard, ScoreCard) else ScoreCard(**scorecard) if scorecard else ScoreCard()


    @property
    def tasks_total(self):
        return self.tasks_easy + self.tasks_medium + self.tasks_hard

    def add(self, decision):
        self.decisions.append(decision)

    @property
    def json(self):
        return {'name': self.name,
                'decisions': [dec.json for dec in self.decisions],
                'tasks_total': self.tasks_total,
                'tasks_easy': self.tasks_easy,
                'tasks_medium': self.tasks_medium,
                'tasks_hard': self.tasks_hard,
                'budget': self.budget,
                'scheduled_days': self.scheduled_days,
                '_id': self.id,
                'desc': self.desc,
                'pred_c': self.pred_c,
                'is_template': True,
                'scorecard': self.scorecard.json
                }


def create_staff_row(team: Team, title: str = 'staff'):
    return {
        'id': team.id,
        'title': f"{title}",
        'values':
            {
                'junior': team.count('junior'),
                'senior': team.count('senior'),
                'expert': team.count('expert')
            },
        'hover': "Juniors cost 3000/mo, have an error rate of 33% and have a throughput of 3 tasks. Seniors cost 4500/mo, have an error rate of 20% and have a throughput of 7 tasks. Experts cost 7000/mo, have an error rate of 5% and have a throughput of 7 tasks."
    }


class UserScenario:
    def __init__(self, **kwargs):
        self.task_queue = kwargs.get('tq') or TaskQueue(**kwargs.get('task_queue', {}))
        self.actual_cost = int(kwargs.get('actual_cost', 0) or 0)
        self.current_day = int(kwargs.get('current_day', 0) or 0)
        self.counter = int(kwargs.get('counter', -1)) # Dont use or -1
        self.decisions = kwargs.get('decisions', []) or []
        self.id = ObjectId(kwargs.get('_id')) or ObjectId()
        self.actions = kwargs.get('actions') or ActionList()
        self.user = kwargs.get('user')
        self.template: Scenario = kwargs.get('template')
        self.template_id: ObjectId = kwargs.get('template_id')
        self.perform_quality_check = False
        self.error_fixing = False
        self.model = kwargs.get('model', 'waterfall') or ""
        self.history_id: ObjectId = kwargs.get('history')
        self.current_wr = None
        if self.model.lower() == 'scrum':
            self.team = ScrumTeam()
        else:
            self.team = Team(str(ObjectId()))

    def __iter__(self):
        return self

    def __next__(self) -> Decision:
        self._eval_counter()
        if self.counter >= len(self.decisions):
            raise StopIteration
        return self.decisions[self.counter]

    def __len__(self) -> int:
        return len(self.decisions)

    def __eq__(self, other):
        if isinstance(other, Scenario):
            return self.id == other.id
        return False

    @property
    def tasks_done(self) -> int:
        return self.task_queue.total_tasks_done

    @property
    def json(self):
        d = {'task_queue': self.task_queue.json,
             'decisions': [dec.json for dec in self.decisions],
             'actual_cost': self.actual_cost,
             'counter': self.counter,
             'current_day': self.current_day,
             'team': self.team.json,
             '_id': self.id,
             'user': self.user,
             'actions': self.actions.json,
             'template_id': self.get_template_id(),
             'model': self.model,
             'history': self.history_id,
             'is_template': False,
             }
        # Remove all items whose value is 'None'
        d = remove_none_values(d)
        return d
    

    def get_template_id(self):
        if self.template:
            return self.template.id
        elif self.template_id:
            return self.template_id
        return None
    
    def set_template_id(self, id):
        self.template_id = id


    def add(self, decision: Decision):
        self.decisions.append(decision)

    def remove(self, index: int):
        del self.decisions[index]

    @property
    def button_rows(self):
        json = []
        d = self.decisions[self.counter]
        if isinstance(d, SimulationDecision):
            for a in d.active_actions or []:
                if (action := self.actions.get(a)) is not None and self.action_is_applicable(action):
                    json.append(action.json)
        else:
            for action in d.actions or []:
                json.append(action.json)
        return json

    @property
    def numeric_rows(self):
        json = []
        d = self.decisions[self.counter]
        for aa in d.active_actions:
            if aa == 'staff-pick':  # ToDo: Make this quick and dirty solution dynamic.
                if isinstance(self.team, Team):
                    json.append(create_staff_row(team=self.team))
                elif isinstance(self.team, ScrumTeam):
                    json.append({
                        'title': "Scrum Management",
                        'values':
                            {
                                'Junior Scrum Master': self.team.junior_master,
                                'Senior Scrum Master': self.team.senior_master,
                                'Product Owner': self.team.po
                            }
                    })
                    for i, team in enumerate(self.team.teams):
                        t = create_staff_row(team=team, title='Scrum Team')
                        json.append(t)

        return json

    def get_max_points(self) -> int:
        return sum([d.get_max_points() for d in self.decisions])

    def work(self, days, meeting, training, overtime, integration_test=False, social=False):
        wp = WorkPackage(days=days, meeting_hours=meeting, training_hours=training,
                         quality_check=self.perform_quality_check,
                         error_fixing=self.error_fixing , day_hours=8 + overtime)
        wr = self.team.work(wp, self.task_queue, integration_test=integration_test, social=social)
        self.current_wr = wr
        self.actual_cost += month_to_day(self.team.salary, days)
        self.current_day += days
        if social:
            self.actual_cost += len(self.team)*1000


    def _eval_counter(self):
        """
        Increases the value of the counter by one of the current decision is done.
        """
        if self.counter == -1:
            self.counter = 0
        else:
            d = self.decisions[self.counter]
            if (not isinstance(d, SimulationDecision)) or (
                    isinstance(d, SimulationDecision) and d.goal.reached(tasks=len(self.task_queue.get(unit_tested=True, integration_tested=True)))):
                self.counter += 1

    def get_decision(self, nr: int = None) -> Optional[Decision]:
        if nr is None:
            nr = self.counter
        if nr < 0:
            return None
        return self.decisions[nr]

    def get_answered_decisions(self):
        return [d for d in self.decisions if not isinstance(d, SimulationDecision)]

    def total_score(self) -> int:
        p = 0
        for d in self.decisions:
            p += d.points
        p += self.time_score()
        p += self.budget_score()
        p += self.quality_score()
        return int(p)

    def time_score(self) -> int:
        actual_time = self.current_day
        scheduled_time = self.template.scheduled_days
        factor = self.template.scorecard.time_limit
        p = self.template.scorecard.time_p

        if actual_time <= scheduled_time:
            return 1*factor
        exceed_ratio = ((actual_time/scheduled_time)-1)*100
        return max(0, int(100-exceed_ratio**p))*factor/100

    def budget_score(self) -> int:
        cost = self.actual_cost
        budget = self.template.budget
        factor = self.template.scorecard.budget_limit
        p = self.template.scorecard.budget_p

        if cost <= budget:
            return 1*factor
        exceed_ratio = ((cost/budget)-1)*100
        return max(0, int(100-exceed_ratio**p))*factor/100

    def quality_score(self) -> int:
        tasks = len(self.task_queue)
        err = len({*self.task_queue.get(bug=True), *self.task_queue.get(done=False), *self.task_queue.get(correct_specification=False)})
        factor = self.template.scorecard.quality_limit
        k = self.template.scorecard.quality_k

        return int((1-(err/tasks))**k * factor)

    def action_is_applicable(self, action):
        """Returns True if an action is applicable. Actions can have restrictions, e.g. model must be scrum or kanban.
        This function checks whether the action's restrictions are applicable in this scenario."""
        applicable = True
        if self.model.lower() not in [x.lower() for x in action.get_restrictions().get('model-pick', [self.model])]:
            applicable = False
        return applicable


