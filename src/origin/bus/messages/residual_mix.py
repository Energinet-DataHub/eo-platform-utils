from dataclasses import dataclass

from origin.bus import Message
from origin.models.residual_mix import \
    ResidualMixEmissions, ResidualMixTechnologyDistribution


@dataclass
class ResidualMixEmissionsUpdate(Message):
    """
    Description of emissions.

    Describes emissions in the general mix within a single sector (pricing
    area), and in a specific time-frame.
    """

    emissions: ResidualMixEmissions


@dataclass
class ResidualMixTechnologyDistributionUpdate(Message):
    """
    Distribution of technologies.

    Describes the distribution of technologies used to produce energy
    in the residual mix within a single sector (pricing area),
    and in a specific time-frame.
    """

    distributions: ResidualMixTechnologyDistribution
