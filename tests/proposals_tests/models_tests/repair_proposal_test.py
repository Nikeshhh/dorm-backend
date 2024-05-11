import pytest

from core.apps.proposals.exceptions import (
    ProposalAccessException,
    ProposalStatusException,
)
from core.apps.users.exceptions import RoleViolationException


@pytest.mark.django_db
def test_proposal_cycle_success(test_proposals, test_worker_user):
    test_proposal = test_proposals[0]
    assert test_proposal.status == 0
    test_proposal.accept(test_worker_user)

    test_proposal.refresh_from_db()
    assert test_proposal.status == 1

    test_proposal.close(test_worker_user)

    test_proposal.refresh_from_db()
    assert test_proposal.status == 2


@pytest.mark.django_db
def test_proposal_accept_fail_not_worker(test_proposals, test_user):
    test_proposal = test_proposals[0]
    assert test_proposal.status == 0

    with pytest.raises(RoleViolationException):
        test_proposal.accept(test_user)


@pytest.mark.django_db
def test_proposal_accept_fail_already_accepted_by_another(
    test_proposals, test_worker_user, other_worker_user
):
    test_proposal = test_proposals[0]
    assert test_proposal.status == 0
    test_proposal.accept(other_worker_user)

    with pytest.raises(ProposalAccessException):
        test_proposal.accept(test_worker_user)


@pytest.mark.django_db
def test_proposal_cycle_success_with_decline_then_accept_by_other(
    test_proposals, test_worker_user, other_worker_user
):
    test_proposal = test_proposals[0]
    assert test_proposal.status == 0
    test_proposal.accept(test_worker_user)

    test_proposal.refresh_from_db()
    assert test_proposal.status == 1

    test_proposal.decline(test_worker_user)

    test_proposal.refresh_from_db()
    assert test_proposal.status == 0
    assert test_proposal.executor is None

    test_proposal.accept(other_worker_user)
    test_proposal.refresh_from_db()
    assert test_proposal.status == 1

    test_proposal.close(other_worker_user)
    test_proposal.refresh_from_db()
    assert test_proposal.status == 2


@pytest.mark.django_db
def test_proposal_close_fail_on_access_fail(
    test_proposals, test_worker_user, other_worker_user
):
    test_proposal = test_proposals[0]
    assert test_proposal.status == 0
    test_proposal.accept(test_worker_user)

    test_proposal.refresh_from_db()
    assert test_proposal.status == 1

    with pytest.raises(ProposalAccessException):
        test_proposal.decline(other_worker_user)

    test_proposal.refresh_from_db()
    assert test_proposal.executor == test_worker_user


@pytest.mark.django_db
def test_proposal_fail_on_repeat_accept(test_proposals, test_worker_user):
    test_proposal = test_proposals[0]
    assert test_proposal.status == 0
    test_proposal.accept(test_worker_user)

    with pytest.raises(ProposalStatusException):
        test_proposal.accept(test_worker_user)
