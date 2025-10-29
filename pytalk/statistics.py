"""Server statistics module for Teamtalk."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ._utils import _get_tt_obj_attribute
from .implementation.TeamTalkPy import TeamTalk5 as sdk

if TYPE_CHECKING:
    from .instance import TeamTalkInstance


class Statistics:
    """represents the statistics of a TeamTalk server."""

    def __init__(
        self,
        teamtalk: TeamTalkInstance,
        statistics: sdk.ServerStatistics,
    ) -> None:
        """Initialize a statistics object.

        Args:
            teamtalk: The pytalk.TeamTalkInstance instance.
            statistics (sdk.ServerStatistics): The sdk.ServerStatistics object.

        """
        self.teamtalk = teamtalk
        self.server = teamtalk.server
        self._statistics = statistics

    def __getattr__(self, name: str) -> object:
        """Try to get the attribute from the ServerStatistics object.

        Args:
            name: The name of the attribute.

        Returns:
            The value of the specified attribute.

        Raises:
            AttributeError: If the specified attribute is not found. This is the
                default behavior. # noqa

        """
        if name in dir(self):
            return self.__dict__[name]
        value = _get_tt_obj_attribute(self._statistics, name)
        if isinstance(value, (bytes, sdk.TTCHAR, sdk.TTCHAR_P)):
            return sdk.ttstr(cast("sdk.TTCHAR_P", value))
        return value

    def refresh(self) -> None:
        """Refresh the server statistics."""
        self._statistics = self.teamtalk.get_server_statistics(timeout=2)._statistics
