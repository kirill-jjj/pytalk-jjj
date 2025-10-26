"""Subscription class for TeamTalk."""

from typing import cast

from .implementation.TeamTalkPy import TeamTalk5 as sdk


class _SubscriptionMeta(type):
    def __getattr__(cls, name: str) -> sdk.UserRight:
        if name == "USER_TEXTMESSAGE":
            name = "SUBSCRIBE_USER_MSG"
        else:
            name = f"SUBSCRIBE_{name}"
        return cast("sdk.UserRight", getattr(sdk.Subscription, name, None))

    def __dir__(cls) -> list[str]:
        return [
            name[10:] for name in dir(sdk.Subscription) if name.startswith("SUBSCRIBE_")
        ]


class Subscription(metaclass=_SubscriptionMeta):
    """A class representing subscriptions in TeamTalk."""
