
from unittest.case import TestCase

from eventsourcing.domain import Aggregate, DomainService, event


class SampleAggregate(Aggregate):
    @event("Created")
    def __init__(self, property):
        self.property = property

    @event("Updated")
    def update(self, property):
        self.property = property


class SampleDomainService(DomainService):
    def execute(self):
        agg1 = SampleAggregate(10)
        agg1.update(20)

        agg2 = SampleAggregate(30)
        agg2.update(40)


class TestDomainService(TestCase):
    def test_collect_aggregates(self):
        with SampleDomainService() as service:
            service.execute()

            changes = service.collect_changes()
            assert len(changes) == 2
            assert changes[0].property == 20
            assert changes[1].property == 40
