"""
Gaming Workforce Observatory - Constantes métier gaming
Données spécifiques à l'industrie du jeu vidéo pour analytics RH
"""

# Départements Gaming Industry
GAMING_DEPARTMENTS = {
    "Programming": {
        "roles": ["Junior Developer", "Software Engineer", "Senior Developer", "Lead Developer", "Principal Engineer"],
        "avg_salary_range": (65000, 180000),
        "key_skills": ["C++", "C#", "Unity", "Unreal Engine", "Python", "JavaScript"]
    },
    "Art & Animation": {
        "roles": ["Junior Artist", "3D Artist", "Senior Artist", "Art Director", "Technical Artist"],
        "avg_salary_range": (45000, 150000),
        "key_skills": ["Maya", "Blender", "Photoshop", "Substance Painter", "ZBrush"]
    },
    "Game Design": {
        "roles": ["Junior Designer", "Game Designer", "Senior Designer", "Lead Designer", "Creative Director"],
        "avg_salary_range": (50000, 160000),
        "key_skills": ["Game Mechanics", "Level Design", "Balancing", "Documentation", "Prototyping"]
    },
    "Quality Assurance": {
        "roles": ["QA Tester", "QA Analyst", "Senior QA", "QA Lead", "QA Manager"],
        "avg_salary_range": (35000, 90000),
        "key_skills": ["Test Planning", "Bug Tracking", "Automation", "Performance Testing"]
    },
    "Production": {
        "roles": ["Assistant Producer", "Producer", "Senior Producer", "Executive Producer"],
        "avg_salary_range": (60000, 200000),
        "key_skills": ["Project Management", "Scrum", "Team Leadership", "Budget Management"]
    }
}

# Major Gaming Studios Worldwide
MAJOR_GAMING_STUDIOS = {
    "Microsoft Gaming": {
        "headquarters": "Redmond, WA, USA",
        "employees": 22000,
        "founded": 2001,
        "notable_games": ["Halo", "Forza", "Age of Empires"],
        "revenue_2024": 18500000000
    },
    "Ubisoft": {
        "headquarters": "Montreuil, France", 
        "employees": 19000,
        "founded": 1986,
        "notable_games": ["Assassin's Creed", "Far Cry", "Tom Clancy's"],
        "revenue_2024": 2130000000
    },
    "Electronic Arts": {
        "headquarters": "Redwood City, CA, USA",
        "employees": 13000,
        "founded": 1982,
        "notable_games": ["FIFA", "Apex Legends", "The Sims"],
        "revenue_2024": 7562000000
    }
}

# Gaming Industry Metrics & Benchmarks
INDUSTRY_BENCHMARKS = {
    "average_tenure_years": {
        "Programming": 3.2,
        "Art & Animation": 2.8,
        "Game Design": 3.5,
        "Quality Assurance": 2.1,
        "Production": 4.2
    },
    "turnover_rates": {
        "Junior": 0.25,
        "Mid": 0.18,
        "Senior": 0.12,
        "Lead": 0.08
    },
    "satisfaction_benchmarks": {
        "Programming": 7.2,
        "Art & Animation": 7.5,
        "Game Design": 8.1,
        "Quality Assurance": 6.8,
        "Production": 7.0
    },
    "crunch_frequency": {
        "Pre-Alpha": 0.1,
        "Alpha": 0.3,
        "Beta": 0.6,
        "Gold Master": 0.9,
        "Post-Launch": 0.2
    }
}

# Neurodiversity in Gaming
NEURODIVERSITY_DATA = {
    "conditions": {
        "ADHD": {
            "prevalence_general": 0.05,
            "prevalence_gaming": 0.12,
            "strengths": ["Hyperfocus", "Creativity", "Problem Solving"],
            "accommodations": ["Noise-canceling headphones", "Flexible breaks", "Written instructions"]
        },
        "Autism Spectrum": {
            "prevalence_general": 0.01,
            "prevalence_gaming": 0.08,
            "strengths": ["Attention to Detail", "Pattern Recognition", "Logical Thinking"],
            "accommodations": ["Quiet workspace", "Structured routines", "Clear communication"]
        },
        "Dyslexia": {
            "prevalence_general": 0.10,
            "prevalence_gaming": 0.15,
            "strengths": ["Visual Thinking", "Creative Solutions", "Big Picture Thinking"],
            "accommodations": ["Text-to-speech", "Visual aids", "Extra time"]
        }
    },
    "performance_multipliers": {
        "Programming": {
            "ADHD": 1.15,
            "Autism Spectrum": 1.30,
            "Dyslexia": 1.05
        },
        "Quality Assurance": {
            "ADHD": 1.10,
            "Autism Spectrum": 1.40,
            "Dyslexia": 1.08
        },
        "Game Design": {
            "ADHD": 1.25,
            "Autism Spectrum": 1.20,
            "Dyslexia": 1.30
        }
    }
}

# Gaming Project Phases
PROJECT_PHASES = {
    "Pre-Production": {
        "duration_months": 6,
        "team_size_multiplier": 0.3,
        "crunch_risk": 0.1
    },
    "Production": {
        "duration_months": 24,
        "team_size_multiplier": 1.0,
        "crunch_risk": 0.4
    },
    "Alpha": {
        "duration_months": 6,
        "team_size_multiplier": 1.2,
        "crunch_risk": 0.6
    },
    "Beta": {
        "duration_months": 4,
        "team_size_multiplier": 1.1,
        "crunch_risk": 0.7
    },
    "Gold Master": {
        "duration_months": 2,
        "team_size_multiplier": 0.9,
        "crunch_risk": 0.9
    },
    "Post-Launch": {
        "duration_months": 12,
        "team_size_multiplier": 0.6,
        "crunch_risk": 0.2
    }
}

# Regional Gaming Markets
REGIONAL_MARKETS = {
    "North America": {
        "market_size_billions": 50.2,
        "average_salary_usd": 95000,
        "major_hubs": ["Los Angeles", "San Francisco", "Seattle", "Montreal"],
        "growth_rate": 0.08
    },
    "Europe": {
        "market_size_billions": 32.8,
        "average_salary_usd": 68000,
        "major_hubs": ["London", "Paris", "Berlin", "Stockholm"],
        "growth_rate": 0.06
    },
    "Asia-Pacific": {
        "market_size_billions": 78.4,
        "average_salary_usd": 45000,
        "major_hubs": ["Tokyo", "Seoul", "Shanghai", "Singapore"],
        "growth_rate": 0.12
    }
}

# Skills & Competencies Matrix
SKILLS_MATRIX = {
    "Technical Skills": [
        "C++", "C#", "Python", "JavaScript", "Unity", "Unreal Engine",
        "Maya", "Blender", "Photoshop", "Git", "Perforce", "Agile/Scrum"
    ],
    "Soft Skills": [
        "Communication", "Teamwork", "Problem Solving", "Creativity",
        "Leadership", "Time Management", "Adaptability", "Critical Thinking"
    ],
    "Gaming Specific": [
        "Game Mechanics Design", "Level Design", "Player Psychology",
        "Monetization", "Live Operations", "Community Management",
        "Platform Certification", "Performance Optimization"
    ]
}
