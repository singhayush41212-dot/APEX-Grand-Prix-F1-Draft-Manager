from dataclasses import dataclass

@dataclass
class Driver:
    name: str
    team: str
    year: int
    ovr: int

@dataclass
class Principal:
    name: str
    ovr: int
    year: int
    special: str

@dataclass
class Car:
    name: str
    team: str
    year: int
    ovr: int

@dataclass
class Team:
    driver1: Driver
    driver2: Driver
    car: Car
    principal: Principal
    name: str = "YOUR DRAFT TEAM"

    @property
    def strength(self) -> float:
        driver_avg = (self.driver1.ovr + self.driver2.ovr) / 2
        return (driver_avg * 0.35) + (self.car.ovr * 0.50) + (self.principal.ovr * 0.15)