from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import math


class PowerTimeOfUse(Enum):
    DAYTIME_ONLY = "daytime_only"
    NIGHT_ONLY = "night_only"
    ANY_TIME = "any_time"

# class Season(Enum):
#     SPRING = "spring"
#     SUMMER = "summer"
#     FALL = "fall"
#     WINTER = "winter"

class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"

    @classmethod
    def from_month(cls, month: int) -> 'Season':
        # Convert month number (0-23) to season enum
        season_map = {
            0: cls.SPRING,  # March
            1: cls.SUMMER,  # June
            2: cls.FALL,    # September
            3: cls.WINTER   # December
        }
        return season_map[month % 4]

@dataclass
class PowerUsage:
    kwh_daily: float
    time_of_use: PowerTimeOfUse

@dataclass
class MarketConnection:
    name: str
    product_types: List[str]  # e.g., ["plants", "eggs", "meat"]
    sales_multiplier: float  # How much this connection improves sales probability


@dataclass
class Resources:
    solar_power_kw: float
    battery_capacity_kwh: float
    daytime_power_available_kwh: float
    water_distance_miles: float
    truck_mpg: float
    initial_soil: float
    available_money_monthly: float
    investment_period_months: int
    work_hours_daily: tuple[float, float]
    outdoor_space_acres: float
    indoor_space_sqft: float
    has_automation_skills: bool
    climate_controlled_sqft: float = 0  # New field for temperature-controlled space
    market_connections: List[MarketConnection] = None
    reinvestment_rate: float = 0.7  # Portion of profits to reinvest vs save for well
    target_savings: float = 25000  # Target amount for well


@dataclass
class InfrastructureUpgrade:
    name: str
    cost: float
    resource_impacts: Dict[str, float]
    monthly_operating_cost: float = 0
    seasonal_benefits: Dict[Season, float] = None  # Multiplier for revenue in each season

    def __post_init__(self):
        if self.seasonal_benefits is None:
            self.seasonal_benefits = {season: 1.0 for season in Season}


@dataclass
class Project:
    name: str
    setup_cost: float
    monthly_cost: float
    monthly_revenue: float
    monthly_savings: float
    space_required_sqft: float
    is_indoor: bool
    daily_hours: float
    water_gallons_daily: float
    power_usage: PowerUsage
    startup_time_months: float
    knowledge_required: int
    sustainability_score: int
    synergy_projects: List[str]
    scalability: int
    automation_potential: int
    product_type: str  # e.g., "plants", "eggs", "meat"
    base_sales_probability: float  # Base probability of selling produced goods
    seasonal_multipliers: Dict[Season, float]  # How season affects production/sales
    climate_controlled_benefit: float  # Revenue multiplier if in climate-controlled space
    startup_time_months: int  # Time to reach production stage
    current_stage: str = "setup"  # Initial stage
    monthly_revenue: float = 0  # Placeholder value

    def update_stage(self):
        if self.current_stage == "setup" and self.startup_time_months == 0:
            self.current_stage = "production"
        elif self.current_stage == "setup":
            self.startup_time_months -= 1

class FarmOptimizer:
    def __init__(self, resources: Resources):
        self.resources = resources
        self.projects = self._initialize_projects()
        self.infrastructure_upgrades = self._initialize_upgrades()

    def _initialize_upgrades(self) -> Dict[str, InfrastructureUpgrade]:
        return {
            "well": InfrastructureUpgrade(
                name="Water Well Installation",
                cost=25000,
                resource_impacts={"water_cost": -1.0},  # Eliminates water transport cost
                monthly_operating_cost=50,  # Electricity for pump, maintenance
                seasonal_benefits={season: 1.0 for season in Season}
            ),
            "greenhouse": InfrastructureUpgrade(
                name="Greenhouse Construction",
                cost=5000,
                resource_impacts={
                    "climate_controlled_sqft": 500,
                    "indoor_space_sqft": 500
                },
                monthly_operating_cost=100,  # Climate control costs
                seasonal_benefits={
                    Season.SPRING: 1.2,
                    Season.SUMMER: 1.0,
                    Season.FALL: 1.3,
                    Season.WINTER: 1.5  # Biggest benefit in winter
                }
            ),
            "hoop_house": InfrastructureUpgrade(
                name="Hoop House",
                cost=2000,
                resource_impacts={
                    "indoor_space_sqft": 300
                },
                monthly_operating_cost=30,
                seasonal_benefits={
                    Season.SPRING: 1.3,
                    Season.SUMMER: 1.1,
                    Season.FALL: 1.2,
                    Season.WINTER: 1.2
                }
            )
        }

    def _initialize_projects(self) -> Dict[str, Project]:
        projects = {}

        # Existing project
        projects["air_plants"] = Project(
            name="Air Cleaning Plants",
            setup_cost=200,
            monthly_cost=30,
            monthly_revenue=100,
            space_required_sqft=50,
            is_indoor=True,
            daily_hours=0.5,
            water_gallons_daily=2,
            power_usage=PowerUsage(1.2, PowerTimeOfUse.DAYTIME_ONLY),
            startup_time_months=3,
            knowledge_required=3,
            sustainability_score=9,
            synergy_projects=["plant_cloning"],
            scalability=6,
            automation_potential=7,
            product_type="plants",
            base_sales_probability=0.7,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.3
            },
            climate_controlled_benefit=1.2,
            startup_time_months= 3,  # Time to reach production stage
            current_stage = "setup",  # Initial stage
            monthly_revenue= 0,  # Placeholder value
            monthly_savings=0,
        )

        # New projects
        projects["rabbit_breeding"] = Project(
            name="Rabbit Breeding",
            setup_cost=500,
            monthly_cost=50,
            space_required_sqft=50,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=5,
            power_usage=PowerUsage(0.5, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=2,
            sustainability_score=8,
            synergy_projects=["compost"],
            scalability=8,
            automation_potential=5,
            product_type="meat",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.1,
                Season.SUMMER: 1.0,
                Season.FALL: 1.2,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.1,
            monthly_revenue=100,
            monthly_savings=0,
        )

        projects["duck_ranching"] = Project(
            name="Duck Ranching",
            setup_cost=1000,
            monthly_cost=100,
            space_required_sqft=100,
            is_indoor=False,
            daily_hours=2,
            water_gallons_daily=10,
            power_usage=PowerUsage(1, PowerTimeOfUse.ANY_TIME),
            startup_time_months=3,
            knowledge_required=3,
            sustainability_score=7,
            synergy_projects=["black_soldier_fly_larvae"],
            scalability=7,
            automation_potential=4,
            product_type="eggs, meat",
            base_sales_probability=0.9,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.1,
                Season.FALL: 1.0,
                Season.WINTER: 0.8
            },
            climate_controlled_benefit=1.0,
            monthly_revenue=100,
            monthly_savings=20,
        )

        projects["black_soldier_fly_larvae"] = Project(
            name="Black Soldier Fly Larvae",
            setup_cost=200,
            monthly_cost=20,
            space_required_sqft=20,
            is_indoor=True,
            daily_hours=0.5,
            water_gallons_daily=1,
            power_usage=PowerUsage(0.2, PowerTimeOfUse.ANY_TIME),
            startup_time_months=1,
            knowledge_required=2,
            sustainability_score=10,
            synergy_projects=["duck_ranching", "edible_insects"],
            scalability=9,
            automation_potential=6,
            product_type="feed",
            base_sales_probability=0.9,
            seasonal_multipliers={
                Season.SPRING: 1.1,
                Season.SUMMER: 1.2,
                Season.FALL: 1.0,
                Season.WINTER: 0.9
            },
            climate_controlled_benefit=1.0,
            monthly_revenue=100,
            monthly_savings=20,
        )

        projects["edible_insects"] = Project(
            name="Edible Insects",
            setup_cost=300,
            monthly_cost=30,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.3, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=9,
            synergy_projects=["black_soldier_fly_larvae"],
            scalability=7,
            automation_potential=5,
            product_type="food",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.1,
                Season.SUMMER: 1.0,
                Season.FALL: 1.2,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.1,
            monthly_revenue=100,
            monthly_savings=20,
        )

        projects["geese_ranching"] = Project(
            name="Geese Ranching",
            setup_cost=800,
            monthly_cost=80,
            space_required_sqft=150,
            is_indoor=False,
            daily_hours=2,
            water_gallons_daily=15,
            power_usage=PowerUsage(1.5, PowerTimeOfUse.ANY_TIME),
            startup_time_months=3,
            knowledge_required=3,
            sustainability_score=7,
            synergy_projects=["duck_ranching"],
            scalability=7,
            automation_potential=4,
            product_type="eggs, meat",
            base_sales_probability=0.85,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.1,
                Season.FALL: 1.0,
                Season.WINTER: 0.8
            },
            climate_controlled_benefit=1.0,
            monthly_revenue=100,
            monthly_savings=20,
        )


        projects["ornamental plants"] = Project(
            name="Plant Cloning",
            setup_cost=300,
            monthly_cost=20,
            monthly_revenue=1000,
            monthly_savings=20,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.4, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=8,
            synergy_projects=["air_plants", "microgreens"],
            scalability=7,
            automation_potential=5,
            product_type="plants",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.2,
        )

        projects["plant_cloning"] = Project(
            name="Plant Cloning",
            setup_cost=300,
            monthly_cost=20,
            monthly_revenue=1000,
            monthly_savings=20,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.4, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=8,
            synergy_projects=["air_plants", "microgreens"],
            scalability=7,
            automation_potential=5,
            product_type="plants",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.2,
        )

        projects["plant_cloning"] = Project(
            name="Plant Cloning",
            setup_cost=300,
            monthly_cost=20,
            monthly_revenue=1000,
            monthly_savings=20,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.4, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=8,
            synergy_projects=["air_plants", "microgreens"],
            scalability=7,
            automation_potential=5,
            product_type="plants",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.2,
        )

        projects["plant_cloning"] = Project(
            name="Plant Cloning",
            setup_cost=300,
            monthly_cost=20,
            monthly_revenue=1000,
            monthly_savings=20,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.4, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=8,
            synergy_projects=["air_plants", "microgreens"],
            scalability=7,
            automation_potential=5,
            product_type="plants",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.2,
        )

        projects["plant_cloning"] = Project(
            name="Plant Cloning",
            setup_cost=300,
            monthly_cost=20,
            monthly_revenue=1000,
            monthly_savings=20,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.4, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=8,
            synergy_projects=["air_plants", "microgreens"],
            scalability=7,
            automation_potential=5,
            product_type="plants",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.2
        )


        projects["plant_cloning"] = Project(
            name="Plant Cloning",
            setup_cost=300,
            monthly_cost=20,
            monthly_revenue=1000,
            monthly_savings=20,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.4, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=8,
            synergy_projects=["air_plants", "microgreens"],
            scalability=7,
            automation_potential=5,
            product_type="plants",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.2
        )
        projects["plant_cloning"] = Project(
            name="Plant Cloning",
            setup_cost=300,
            monthly_cost=20,
            monthly_revenue=1000,
            monthly_savings=20,
            space_required_sqft=30,
            is_indoor=True,
            daily_hours=1,
            water_gallons_daily=2,
            power_usage=PowerUsage(0.4, PowerTimeOfUse.ANY_TIME),
            startup_time_months=2,
            knowledge_required=3,
            sustainability_score=8,
            synergy_projects=["air_plants", "microgreens"],
            scalability=7,
            automation_potential=5,
            product_type="plants",
            base_sales_probability=0.8,
            seasonal_multipliers={
                Season.SPRING: 1.2,
                Season.SUMMER: 1.0,
                Season.FALL: 1.1,
                Season.WINTER: 1.0
            },
            climate_controlled_benefit=1.2
        )

        return projects



    def check_power_feasibility(self, projects: List[Project]) -> bool:
        daytime_power = sum(p.power_usage.kwh_daily
                            for p in projects
                            if p.power_usage.time_of_use == PowerTimeOfUse.DAYTIME_ONLY)

        battery_power = sum(p.power_usage.kwh_daily
                            for p in projects
                            if p.power_usage.time_of_use in [PowerTimeOfUse.NIGHT_ONLY, PowerTimeOfUse.ANY_TIME])

        return (daytime_power <= self.resources.daytime_power_available_kwh and
                battery_power <= self.resources.battery_capacity_kwh * 0.8)  # 80% DOD for battery longevity

    def calculate_water_costs(self, gallons_daily: float) -> float:
        trips_per_month = (gallons_daily * 30) / 100  # assumin 100 gallon tank
        miles_per_month = trips_per_month * self.resources.water_distance_miles * 2
        gas_cost_per_mile = 3.50 / self.resources.truck_mpg
        return miles_per_month * gas_cost_per_mile

    def calculate_market_adjusted_revenue(self, project: Project, season: Season) -> float:
        """Calculate revenue adjusted for market connections and season"""
        base_revenue = project.monthly_revenue

        # Apply seasonal multiplier
        revenue = base_revenue * project.seasonal_multipliers[season]

        # Apply climate control benefit if applicable
        if project.is_indoor and project.space_required_sqft <= self.resources.climate_controlled_sqft:
            revenue *= project.climate_controlled_benefit

        # Apply market connection multipliers
        if self.resources.market_connections:
            relevant_connections = [
                conn for conn in self.resources.market_connections
                if project.product_type in conn.product_types
            ]
            if relevant_connections:
                max_multiplier = max(conn.sales_multiplier for conn in relevant_connections)
                revenue *= max_multiplier

        # Apply base sales probability
        revenue *= project.base_sales_probability

        return revenue

    def calculate_infrastructure_roi(self, upgrade: InfrastructureUpgrade,
                                     current_projects: List[Project],
                                     projection_months: int = 12) -> float:
        """Calculate ROI for an infrastructure upgrade considering seasonal benefits"""
        total_cost = upgrade.cost + (upgrade.monthly_operating_cost * projection_months)
        total_benefit = 0

        # Calculate monthly benefits across seasons
        for month in range(projection_months):
            season = Season(["spring", "summer", "fall", "winter"][month % 4])

            # Calculate benefit to existing projects
            for project in current_projects:
                if project.is_indoor:
                    # Calculate revenue difference with upgrade
                    current_revenue = self.calculate_market_adjusted_revenue(project, season)

                    # Simulate revenue with upgrade
                    if "climate_controlled_sqft" in upgrade.resource_impacts:
                        project_with_upgrade = project
                        revenue_with_upgrade = current_revenue * upgrade.seasonal_benefits[season]

                        total_benefit += revenue_with_upgrade - current_revenue

        return (total_benefit - total_cost) / total_cost if total_cost > 0 else 0

    def calculate_project_score(self, project: Project, selected_projects: List[Project]) -> float:
        # Calculate base ROI considering water costs and seasonal adjustments
        monthly_water_cost = self.calculate_water_costs(project.water_gallons_daily)
        monthly_profit = (project.monthly_revenue + project.monthly_savings -
                          project.monthly_cost - monthly_water_cost)
        simple_roi = monthly_profit / project.setup_cost

        # Consider synergy with existing projects
        synergy_bonus = sum(1 for p in selected_projects
                            if project.name in p.synergy_projects
                            or p.name in project.synergy_projects)

        # Consider automation potential (if user has automation skills)
        automation_bonus = (project.automation_potential / 10) if self.resources.has_automation_skills else 0

        # Consider scalability potential
        scalability_bonus = project.scalability / 10

        # Combine scores with weights (adjust weights as needed)
        return (simple_roi * 0.4 +  # 40% weight on ROI
                synergy_bonus * 0.2 +  # 20% weight on synergies
                automation_bonus * 0.2 +  # 20% weight on automation potential
                scalability_bonus * 0.2)  # 20% weight on scalability
    


    def optimize_with_infrastructure(self, projection_months=24, aggressive_reinvestment=12):
        current_projects = []
        planned_upgrades = []
        available_budget = self.resources.available_money_monthly * self.resources.investment_period_months
        financial_projection = {
            'monthly_details': [],  # Track details for each month
            'monthly_profits': [],
            'accumulated_savings': [],
            'infrastructure_investments': [],
            'well_savings': []
        }

        available_hours = self.resources.work_hours_daily[0]
        available_indoor_space = self.resources.indoor_space_sqft
        available_outdoor_space = self.resources.outdoor_space_acres * 43560  # Convert acres to sqft
        accumulated_savings = 0  # Track accumulated savings explicitly

        # Monthly projection loop
        for month in range(projection_months):
            season = Season.from_month(month)
            monthly_report = {"month": month + 1, "actions": [], "profit": 0, "savings": 0}

            # Update project stages and calculate monthly revenue
            for project in current_projects:
                project.update_stage()

                if project.current_stage == "production":
                    project.monthly_revenue = calculate_monthly_revenue(project)
                else:
                    project.monthly_revenue = 0

            # ... (rest of the optimization logic, including project selection, resource allocation, and financial tracking)

            # Allocate funds to projects based on available budget and project stage
            for project in self.projects.values():
                if project not in current_projects and project.current_stage == "setup":
                    required_funds = project.setup_cost - project.funded_so_far
                    if required_funds <= available_budget:
                        # Allocate funds to the project
                        project.funded_so_far += required_funds
                        available_budget -= required_funds
                        if project.funded_so_far >= project.setup_cost:
                            project.current_stage = "growth"
                        monthly_report["actions"].append(f"Funded {project.name}")

           
            # Calculate monthly revenue and costs
            monthly_revenue = sum(
                self.calculate_market_adjusted_revenue(project, season)
                for project in current_projects
            )
            monthly_costs = sum(project.monthly_cost for project in current_projects)
            water_costs = sum(self.calculate_water_costs(p.water_gallons_daily)
                              for p in current_projects)

            monthly_profit = monthly_revenue - monthly_costs - water_costs
            monthly_report["profit"] = monthly_profit

            # Reinvest profits aggressively
            reinvestment_amount = monthly_profit + available_budget
            affordable_upgrades = [
                upgrade for upgrade in self.infrastructure_upgrades.values()
                if upgrade not in planned_upgrades and upgrade.cost <= reinvestment_amount
            ]

            # Select the best ROI upgrade
            if affordable_upgrades:
                best_upgrade = max(
                    affordable_upgrades,
                    key=lambda u: self.calculate_infrastructure_roi(u, current_projects, projection_months - month)
                )
                planned_upgrades.append(best_upgrade)
                reinvestment_amount -= best_upgrade.cost

                # Apply upgrade benefits
                for resource, impact in best_upgrade.resource_impacts.items():
                    if hasattr(self.resources, resource):
                        current_value = getattr(self.resources, resource)
                        setattr(self.resources, resource, current_value + impact)

                monthly_report["actions"].append(f"Implemented upgrade: {best_upgrade.name}")

            # Update savings and budget
            savings_amount = reinvestment_amount * (1 - self.resources.reinvestment_rate)
            accumulated_savings += savings_amount
            available_budget = reinvestment_amount * self.resources.reinvestment_rate
            monthly_report["savings"] = accumulated_savings

            # Update financial projection
            financial_projection['monthly_details'].append(monthly_report)
            financial_projection['monthly_profits'].append(monthly_profit)
            financial_projection['accumulated_savings'].append(accumulated_savings)
            financial_projection['infrastructure_investments'].append(
                sum(upgrade.cost for upgrade in planned_upgrades)
            )
            financial_projection['well_savings'].append(accumulated_savings)


        return current_projects, planned_upgrades, financial_projection

    def generate_enhanced_report(self, projects: List[Project],
                                 upgrades: List[InfrastructureUpgrade],
                                 financial_projection: Dict) -> str:
        """Generate detailed report including monthly breakdown and infrastructure analysis."""
        report = "Enhanced Farm Optimization Report\n\n"

        # Financial Summary
        report += "Financial Projection Summary:\n"
        report += f"Total Months Projected: {len(financial_projection['monthly_profits'])}\n"
        report += f"Final Accumulated Savings: ${financial_projection['accumulated_savings'][-1]:.2f}\n"
        report += f"Total Infrastructure Investment: ${financial_projection['infrastructure_investments'][-1]:.2f}\n"
        report += f"Progress Toward Well: {(financial_projection['well_savings'][-1] / self.resources.target_savings * 100):.1f}%\n\n"

        # Monthly Breakdown
        report += "Monthly Breakdown:\n"
        for month_detail in financial_projection['monthly_details']:
            report += f"Month {month_detail['month']}:\n"
            for action in month_detail["actions"]:
                report += f"  - {action}\n"
            report += f"  Profit: ${month_detail['profit']:.2f}\n"
            report += f"  Savings: ${month_detail['savings']:.2f}\n\n"

        # Project Details with Seasonal Analysis
        report += "Project Performance by Season:\n"
        for project in projects:
            report += f"\n{project.name}\n"
            for season in Season:
                revenue = self.calculate_market_adjusted_revenue(project, season)
                report += f"   {season.value}: ${revenue:.2f}/month\n"

        return report


# Example usage
resources = Resources(
    solar_power_kw=10,
    battery_capacity_kwh=28,
    daytime_power_available_kwh=35,  # Average available during peak sun
    water_distance_miles=35,
    truck_mpg=15,
    initial_soil=0,
    available_money_monthly=500,
    investment_period_months=12,
    work_hours_daily=(8, 10),
    outdoor_space_acres=0.5,
    indoor_space_sqft=200,
    has_automation_skills=True
)

optimizer = FarmOptimizer(resources)
recommended_projects, recommended_upgrades, financial_projection = optimizer.optimize_with_infrastructure()

# Generate and print report
print(optimizer.generate_enhanced_report(recommended_projects, recommended_upgrades, financial_projection))