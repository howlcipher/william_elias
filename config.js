const config = {
    "personal": {
        "name": "William Elias",
        "title": "Senior DevOps / Platform Engineer",
        "tagline": "CI/CD Automation | Production Reliability | AI-Enabled Engineering",
        "location": "Michigan",
        "remote": "Open to U.S. Remote Roles",
        "photo": "1778619951750.jpg",
        "email": "WylElias.123@gmail.com",
        "phone": "586.438.6057",
        "linkedin": "https://linkedin.com/in/wylelias",
        "github": "https://github.com/howlcipher",
        "resumePdf": "William_Elias_Resume.pdf",
        "sourceRepo": "https://github.com/howlcipher/william_elias",
        "sourceBranch": "main"
    },
    "seo": {
        "canonicalUrl": "https://howlcipher.github.io/william_elias/",
        "siteName": "William Elias | Senior DevOps / Platform Engineer",
        "knowsAbout": [
            "DevOps",
            "Platform Engineering",
            "Azure DevOps",
            "CI/CD",
            "Release Automation",
            "Production Reliability",
            "Python",
            "Go",
            "C# / .NET",
            "PowerShell",
            "Observability",
            "Agentic AI",
            "RAG",
            "MCP"
        ]
    },
    "summary": "Senior DevOps and platform engineer with 10+ years spanning software delivery, production operations, infrastructure, networking, databases, and automation. Designed the standard .NET CI/CD and release pattern for an estate of ~60 internal web applications, remediated exposed credentials across 100+ repositories, co-led production server migration and DR cutovers, and scripted the retirement of 300+ legacy applications. Builds secure, tested internal tooling in C#/.NET, Python, PowerShell, Go, and SQL Server; helped establish Application Insights as the team observability standard and drove adoption across legacy applications. Hands-on with Azure DevOps, GitHub Actions, Azure Key Vault, Azure Monitor, KQL, and applied AI/agentic engineering layered on top of a production platform and automation foundation.",
    "stats": [
        {
            "value": "~60",
            "label": "Applications in CI/CD delivery-standardization scope"
        },
        {
            "value": "100+",
            "label": "Repositories credential-remediated"
        },
        {
            "value": "300+",
            "label": "Legacy applications retired"
        }
    ],
    "skills": [
        {
            "category": "DevOps & Release Engineering",
            "icon": "fa-cloud",
            "tags": [
                "Azure DevOps",
                "Azure DevOps YAML",
                "Classic Release",
                "CI/CD",
                "Pipeline as Code",
                "Reusable Templates",
                "Deployment Groups",
                "GitHub Actions",
                "Git",
                "Bitbucket",
                "Release Gates"
            ]
        },
        {
            "category": "Automation & Software Engineering",
            "icon": "fa-code",
            "tags": [
                "Python",
                "PowerShell",
                "C#",
                "Go",
                "SQL",
                ".NET",
                "ASP.NET Core",
                "REST APIs",
                "FastAPI"
            ]
        },
        {
            "category": "Security & Identity",
            "icon": "fa-shield-halved",
            "tags": [
                "Azure Key Vault",
                "Managed Identity",
                "OAuth 2.0",
                "IAM",
                "Credential Remediation",
                "PII controls",
                "CodeQL",
                "Bandit"
            ]
        },
        {
            "category": "Observability & Reliability",
            "icon": "fa-chart-line",
            "tags": [
                "Application Insights",
                "Azure Monitor",
                "KQL",
                "Serilog",
                "Structured Logging",
                "Incident Triage",
                "RCA",
                "SLA Support"
            ]
        },
        {
            "category": "Infrastructure & Networking",
            "icon": "fa-network-wired",
            "tags": [
                "IIS",
                "Windows Server",
                "Active Directory",
                "SQL Server",
                "Load Balancers",
                "Firewalls",
                "Docker",
                "Docker Compose",
                "Helm",
                "Rancher Desktop"
            ]
        },
        {
            "category": "AI & Agentic Systems",
            "icon": "fa-robot",
            "tags": [
                "MCP",
                "RAG",
                "ChromaDB",
                "Vector Search",
                "Embeddings",
                "Multi-Agent Routing",
                "LLM APIs",
                "AI Guardrails",
                "Prompt-Injection Defenses",
                "Human-in-the-Loop Workflows"
            ]
        }
    ],
    "experience": [
        {
            "date": "Feb 2023 - Present",
            "title": "Production Support Engineer - DevOps & Automation",
            "company": "Stellantis Financial Services US",
            "location": "Auburn Hills, MI \u00b7 Remote",
            "achievements": [
                "Engineering work spans CI/CD and release standardization, production reliability, secrets remediation, internal platform development, observability, server migration, and application-estate reduction in a regulated financial-services environment.",
                "Designed the standard .NET build and release pattern for an estate of ~60 internal apps across five servers, replacing inconsistent deployment paths with reusable automation, release definitions, and deployment guardrails.",
                "Build production operational tooling with C#/.NET, Python, PowerShell, Go, and SQL Server, including credential-remediation utilities, Key Vault migration tooling, and a modular internal support platform with automated testing, auditability, and security controls.",
                "Support production incidents and releases while coordinating across Windows, DBA, IAM, firewall, and load-balancer teams to maintain environment readiness and production reliability."
            ]
        },
        {
            "date": "Jul 2020 - Feb 2023",
            "title": "DevOps Engineer - Python Automation",
            "company": "HBK - Hottinger Br\u00fcel & Kj\u00e6r",
            "location": "Southfield, Michigan / Remote",
            "achievements": [
                "Built Python-based XML processing automation that reduced data-processing time by 60%.",
                "Automated SQL output processing and operational workflows with Python, saving 40+ hours per month of manual effort.",
                "Developed database configuration and automation tooling that streamlined customer onboarding and reduced repetitive environment setup.",
                "Built NSIS installer/uninstaller packages, maintained Git-based development workflows and tooling, and supported application deployment and technical troubleshooting."
            ]
        }
    ],
    "selectedEngineeringPrograms": [
        {
            "name": "CI/CD & Release Engineering",
            "pdfBullet": "Designed the standard .NET CI/CD and release pattern for a ~60-application, five-server estate with no prior consistent path; 28 of 60 wired and build-verified, 27 green.",
            "bullets": [
                "Designed the standard .NET build/release pattern for an estate of approximately 60 internal web applications across five servers that previously had no consistent deployment path.",
                "Built a repository-to-server-to-deployment-path inventory, a generator that emits build pipelines, and multi-tier Azure DevOps Classic Release definitions.",
                "28 of approximately 60 applications are wired and build-verified, with 27 currently green.",
                "Deployment-path dry-run validation caught a mapping defect in the generator that would have mirrored the wrong application into six production folders.",
                "Also built reusable Python/.NET pipeline templates and a WSL2 + Rancher Desktop container-host proof of concept behind IIS ARR."
            ],
            "technology": [
                "Azure DevOps YAML",
                "Azure DevOps Classic Release",
                "Deployment Groups",
                "Azure DevOps REST APIs",
                "PowerShell",
                "Python",
                "IIS",
                "MSBuild",
                ".NET Framework",
                ".NET 8",
                "WSL2",
                "Rancher Desktop",
                "IIS ARR"
            ]
        },
        {
            "name": "Credential Hygiene & Secrets Remediation",
            "pdfBullet": "Removed exposed credentials from 100+ repositories via Git-history remediation, then built a .NET 8 discovery/Key Vault migration utility backed by 62 automated tests.",
            "bullets": [
                "Built audit and Git-history remediation tooling that removed exposed credentials from 100+ repositories, including historical branches.",
                "Built a purpose-built .NET 8 utility for hash-only secret discovery, classification, Azure Key Vault migration, and integrity-verified rollback.",
                "Backed by 62 automated tests.",
                "Measured server run: 2,832 files scanned, 67 distinct secrets identified, 25 seconds.",
                "Self-review identified and corrected a migration-path integrity flaw before rollout."
            ],
            "technology": [
                ".NET 8",
                "C#",
                "Spectre.Console",
                "xUnit",
                "Azure Key Vault",
                "Managed Identity",
                "Python",
                "PowerShell",
                "Git history rewriting"
            ]
        },
        {
            "name": "Server Migration & DR Cutover",
            "pdfBullet": "Co-led build-out of four new production/test servers and coordinated a zero-downtime cutover from legacy infrastructure.",
            "bullets": [
                "Co-led build-out of four new production/test servers.",
                "Coordinated across OS configuration, Windows Server, IIS, Active Directory, firewall, application migration, databases, and load balancers.",
                "Helped coordinate a zero-downtime cutover from legacy infrastructure."
            ],
            "technology": [
                "Windows Server",
                "IIS",
                "Active Directory",
                "PowerShell",
                "SQL Server",
                "Load Balancers"
            ]
        },
        {
            "name": "Internal Web Apps & Support Portal",
            "pdfBullet": "Expanded a query extractor into a modular internal support portal with per-module access policies, a permanently retained SOX audit trail, and 156 automated tests.",
            "bullets": [
                "Expanded a single-purpose query extractor into a modular ASP.NET Core internal support platform.",
                "Included a modular framework, per-module access policies, a permanently retained SOX audit trail, and DBA approve-only deployment scripts.",
                "Added a live-object diff, pre-CAB dashboard, and request tracking integrated with the existing service-desk process.",
                "Covered by 156 automated tests."
            ],
            "technology": [
                "ASP.NET Core 8",
                "Razor Pages",
                "C#",
                "xUnit",
                "SQLite",
                "SQL Server",
                "Serilog",
                "Application Insights",
                "Windows Authentication",
                "DiffPlex",
                "FastAPI"
            ]
        },
        {
            "name": "Observability & Telemetry",
            "pdfBullet": "Helped establish Application Insights as the team standard, added structured logging estate-wide, authored the KQL library, and built a usage-based sunset list.",
            "bullets": [
                "Contributed to the Application Insights proof of concept that became the team standard.",
                "Drove adoption across the legacy application estate.",
                "Added structured logging to applications that previously lacked it.",
                "Authored the team's KQL query library.",
                "Used resulting usage telemetry to build an evidence-based application sunset list."
            ],
            "technology": [
                "Application Insights",
                "Azure Monitor",
                "KQL",
                "Serilog",
                ".NET"
            ]
        },
        {
            "name": "Python Ops Automation & Estate Reduction",
            "pdfBullet": "Built Python automation for database copying, payload triage, and report generation, then scripted the retirement of 300+ legacy applications.",
            "bullets": [
                "Built PII-masked production-to-lower-environment database copying and failed-payload triage.",
                "Developed event-driven query-to-email workflows, XML/log parsing, and vendor report-to-Excel conversion.",
                "Hosted and supported Python applications on IIS.",
                "Created multi-string source search for decommission planning.",
                "Scripted the retirement of 300+ unused legacy applications and standardized team Python tooling around uv."
            ],
            "technology": [
                "Python",
                "uv",
                "FastAPI",
                "SQL Server",
                "PowerShell",
                "IIS",
                "Go"
            ]
        }
    ],
    "projects": [
        {
            "name": "Multi-Agent Engineering Library",
            "subtitle": "Open-source AI context system for terminal agents",
            "link": "https://github.com/howlcipher/ai_knowledge_library",
            "highlights": [
                "Built a filesystem-based knowledge and rules library that loads one canonical rulebook, skill set, and profile context into Claude Code, Codex, and Gemini CLI alike, so agent behavior stays consistent across every terminal assistant.",
                "Ships 40 domain skills with hallucination guardrails, MCP integrations, and ChromaDB context pruning, packaged with Docker, Helm, and a cross-platform installer, guarded by GitHub Actions running CodeQL, Bandit SAST, and cross-platform tests."
            ],
            "tags": [
                "Python",
                "Go",
                "Docker",
                "Helm",
                "GitHub Actions",
                "MCP",
                "ChromaDB"
            ]
        },
        {
            "name": "AI Router",
            "subtitle": "Local multi-provider coding-agent orchestrator",
            "link": "https://github.com/howlcipher/ai_router",
            "highlights": [
                "Built a local orchestrator that routes coding-agent tasks across Claude Code, Codex CLI, and Antigravity using task classification, provider health checks, fallback logic, circuit breakers, and cooldown handling.",
                "Tracks run history in SQLite with structured JSONL run artifacts and captured Git diffs, and enforces safe, Git-aware edit-mode guardrails so agent-driven changes stay reviewable."
            ],
            "tags": [
                "Python",
                "Claude Code",
                "Codex CLI",
                "Antigravity",
                "SQLite",
                "Circuit Breakers"
            ]
        },
        {
            "name": "Zero",
            "subtitle": "Experimental AI-first language and toolchain, written in Go",
            "link": "https://github.com/howlcipher/zero",
            "highlights": [
                "Built a Lisp-like language and compiler toolchain in Go, including a lexer, parser, typed AST/IR, and bytecode VM, with a WebAssembly compilation target and a capability-based security model.",
                "Explores constrained AI code generation against the language's typed IR, with local Ollama integration for offline generation."
            ],
            "tags": [
                "Go",
                "Compilers",
                "WebAssembly",
                "Bytecode VM",
                "Ollama"
            ]
        },
        {
            "name": "Baseball Optimizer",
            "subtitle": "Rust backend for lineup and roster optimization",
            "link": "https://github.com/howlcipher/baseball_optimizer",
            "highlights": [
                "Migrated a performance-sensitive optimization backend to Rust and Axum with a SQLite-backed REST API, containerized with Docker and Docker Compose.",
                "Built automated end-to-end tests with pytest covering the API and model-evaluation paths, wired into CI."
            ],
            "tags": [
                "Rust",
                "Axum",
                "SQLite",
                "Docker",
                "pytest"
            ]
        },
        {
            "name": "RedrawUS",
            "subtitle": "Geospatial data-analysis and visualization platform",
            "link": "https://github.com/howlcipher/redistricting-map",
            "highlights": [
                "Built a multi-state geospatial analysis pipeline combining Python and R simulation tooling with an interactive JavaScript mapping frontend, persistent browser caching, Web Workers, and multi-tier automated testing.",
                "Uses GeoPandas, Shapely, GerryChain, R redistricting tooling, Leaflet, IndexedDB, Playwright, Vitest, and pytest to process, visualize, and validate large geographic datasets."
            ],
            "tags": [
                "Python",
                "R",
                "Geospatial",
                "JavaScript",
                "Playwright",
                "Data Engineering"
            ]
        },
        {
            "name": "Password Arena",
            "subtitle": "Adversarial security-learning sandbox",
            "link": "https://github.com/howlcipher/password_arena",
            "highlights": [
                "Built a local attacker-versus-defender simulation for evaluating synthetic password strength and adaptive strategies under bounded attack budgets, with reproducible experiments, security guardrails, metrics, and audit-style reporting.",
                "Designed explicit safety boundaries around synthetic credentials, bounded guessing, CSPRNG generation, reproducible test modes, and automated quality checks with pytest, mypy, and Ruff."
            ],
            "tags": [
                "Python",
                "Cybersecurity",
                "Docker",
                "pytest",
                "Simulation"
            ]
        }
    ],
    "aiEngineeringCapabilities": [
        {
            "tier": "Coding Agents",
            "items": [
                "Claude Code",
                "Codex CLI",
                "Gemini CLI / Antigravity"
            ]
        },
        {
            "tier": "Orchestration",
            "items": [
                "Multi-Agent Routing",
                "Provider Fallback",
                "Task Classification",
                "Circuit Breakers"
            ]
        },
        {
            "tier": "Context & Retrieval",
            "items": [
                "MCP",
                "RAG",
                "ChromaDB",
                "Vector Search",
                "Embeddings"
            ]
        },
        {
            "tier": "Local AI",
            "items": [
                "Ollama",
                "Local LLMs",
                "Provider-Agnostic Workflows"
            ]
        },
        {
            "tier": "Safety & Reliability",
            "items": [
                "Prompt-Injection Defenses",
                "Human-in-the-Loop",
                "Agent Guardrails",
                "Structured Audit/Run Artifacts"
            ]
        }
    ],
    "additionalExperience": [
        {
            "company": "Intrepid Control Systems",
            "title": "Quality Assurance Developer",
            "date": "Mar 2020",
            "summary": "Developed and executed Mocha tests for internal applications and debugged APIs across software and hardware integrations."
        },
        {
            "company": "Project Worldwide",
            "title": "Network Engineer",
            "date": "Jan 2020 - Mar 2020",
            "summary": "Configured Cisco switching and Meraki wireless infrastructure, created network/IP-addressing standards, and supported multi-state network migrations with minimal downtime."
        },
        {
            "company": "Ford Motor Company",
            "title": "Network Engineer",
            "date": "Sep 2019 - Dec 2019",
            "summary": "Implemented standardized network configurations, built documentation and IP-management systems, and supported enterprise network migrations."
        },
        {
            "company": "Trendset Communications Group",
            "title": "Network Engineer",
            "date": "Sep 2015 - Jun 2019",
            "summary": "Administered and audited network infrastructure across ports, IP addressing, VLANs, and device configurations while supporting production connectivity and availability."
        }
    ],
    "education": [
        {
            "icon": "fa-user-graduate",
            "degree": "M.S. Cyber Defense - In Progress",
            "school": "Dakota State University",
            "year": ""
        },
        {
            "icon": "fa-university",
            "degree": "B.S. Information Technology",
            "school": "Colorado State University Global Campus",
            "year": ""
        },
        {
            "icon": "fa-graduation-cap",
            "degree": "B.B.A. Business Administration",
            "school": "Rochester College",
            "year": ""
        },
        {
            "icon": "fa-certificate",
            "degree": "CCNA - previously held",
            "school": "Cisco Networking Academy",
            "year": "2014 - 2017"
        }
    ],
    "footerText": "\u00a9 2026 William Elias. All rights reserved."
};
