const config = {
    personal: {
        name: "William Elias",
        title: "Automation & Systems Engineer",
        tagline: "Python • Go • PowerShell • SQL | DevOps & Infrastructure | AI-Assisted Development",
        email: "WylElias.123@gmail.com",
        phone: "586.438.6057",
        linkedin: "https://linkedin.com/in/wylelias",
        github: "https://github.com/howlcipher",
        resumePdf: "William_Elias_Resume.pdf",
        sourceRepo: "https://github.com/howlcipher/william_elias"
    },
    summary: "Automation and systems engineer with 10+ years of experience across software development, infrastructure, DevOps, networking, and production support. Builds Python, Go, PowerShell, and SQL solutions for backend services, APIs, data processing, deployment pipelines, system integrations, and operational tooling. Delivered automation that reduced processing time by 60%, saved more than 40 hours per month, and improved deployment workflows by 30%. Combines enterprise operations experience with secure engineering practices, troubleshooting, and AI-assisted development.",
    skills: [
        {
            category: "Programming & Development",
            icon: "fa-code",
            tags: ["Python", "Go", "C#", ".NET Framework", "PowerShell", "SQL", "REST APIs", "ETL"]
        },
        {
            category: "DevOps & Delivery",
            icon: "fa-cloud",
            tags: ["Azure DevOps", "CI/CD", "Git", "Bitbucket", "GitHub Actions", "Docker", "Helm", "IIS", "NSIS"]
        },
        {
            category: "Cloud, Monitoring & Security",
            icon: "fa-server",
            tags: ["Application Insights", "Key Vault", "Azure Monitor", "Bandit SAST", "Log Monitoring"]
        },
        {
            category: "Data & Systems",
            icon: "fa-server",
            tags: ["SQL Server", "SQLite", "Database Migrations", "Stored Procedures", "Windows Server", "Job Scheduling"]
        },
        {
            category: "Networking",
            icon: "fa-network-wired",
            tags: ["Cisco", "Meraki", "VLANs", "Firewalls", "Packet Capture", "Network Standards"]
        },
        {
            category: "AI & Knowledge Systems",
            icon: "fa-robot",
            tags: ["LLM API Integration", "Multi-Agent Orchestration", "ChromaDB", "RAG", "Prompt Engineering"]
        }
    ],
    experience: [
        {
            date: "Feb 2023 - Present",
            title: "Production Support Engineer (Automation & CI/CD)",
            company: "Stellantis Financial Services",
            location: "Auburn Hills, MI",
            achievements: [
                "Developed a Python automation system converting TXT reports to Excel, saving several hours of manual work daily while improving overall system reliability.",
                "Built Go and PowerShell deployment tools that improved deployment processes by 30 percent.",
                "Implemented database migration strategies between environments with zero data loss.",
                "Managed IIS applications including configuration, troubleshooting, and performance optimization.",
                "Led weekly releases and deployments using Git workflows and Bitbucket.",
                "Developed scripts for log parsing, anomaly detection, and data validation to support production operations.",
                "Architected an internal Jira and SharePoint knowledge platform that detects documentation drift and supports natural-language questions for onboarding and troubleshooting.",
                "Built a production support portal that centralizes team links, runbooks, and documentation in a searchable hub."
            ]
        },
        {
            date: "Jul 2020 - Feb 2023",
            title: "DevOps Engineer (Python Automation)",
            company: "HBK Engineering Solutions",
            location: "Southfield, MI",
            achievements: [
                "Created a Python and Tkinter XML-output automation system that reduced data-processing time by 60 percent.",
                "Automated SQL output processing with Python, saving more than 40 hours per month.",
                "Developed database configuration tools that streamlined customer onboarding workflows.",
                "Built installer and uninstaller packages with NSIS for reliable application deployment.",
                "Maintained Git workflows and developer tooling, and provided live technical troubleshooting for customers."
            ]
        },
        {
            date: "Mar 2020 - Apr 2020",
            title: "QA Developer",
            company: "Intrepid Control Systems",
            location: "Madison Heights, MI",
            achievements: [
                "Wrote and executed Mocha test cases for internal software applications.",
                "Debugged and validated APIs across software and hardware integrations."
            ]
        },
        {
            date: "Jan 2020 - Mar 2020",
            title: "Network Engineer",
            company: "Project Worldwide",
            location: "",
            achievements: [
                "Configured Cisco switches and Meraki access points across multiple enterprise locations.",
                "Developed network documentation standards and IP-addressing schemes.",
                "Executed multi-state network migrations with minimal operational downtime."
            ]
        },
        {
            date: "Sep 2019 - Dec 2019",
            title: "Network Standards Engineer",
            company: "Ford Motor Company",
            location: "",
            achievements: [
                "Implemented global network configuration standards across distributed enterprise infrastructure.",
                "Created documentation templates and IP-management databases to improve scalability and consistency.",
                "Supported large-scale network migrations through planning and technical execution."
            ]
        },
        {
            date: "Sep 2015 - Jun 2019",
            title: "IT Network Engineer",
            company: "Trendset Communications Group",
            location: "",
            achievements: [
                "Enforced network standards and performed audits covering ports, IP addresses, and VLANs.",
                "Maintained configuration files across diverse network equipment environments.",
                "Provided tiered production support for critical network infrastructure and organizational uptime."
            ]
        }
    ],
    projects: [
        {
            name: "AI Knowledge Library",
            subtitle: "Multi-agent orchestration platform - Python, Go",
            highlights: [
                "Architected and built a platform that routes engineering work across Claude, Gemini, and local Ollama models using shared skills, rules, and project context.",
                "Implemented skill routing with keyword matching and ChromaDB semantic-search fallback to surface relevant domain knowledge.",
                "Established production-grade quality with a 148-test Python and Go suite, Bandit SAST scanning, and pre-push CI gates.",
                "Packaged as a Go-built CLI installer with a Helm chart and Docker/GitHub Actions deployment.",
            ],
            tags: ["Python", "Go", "Claude Code", "Gemini CLI", "ChromaDB", "Helm", "Docker", "GitHub Actions"]
        },
        {
            name: "Career Agent Core",
            subtitle: "AI-powered job search assistant - Go",
            highlights: [
                "Architected and built a Go service that aggregates remote job postings and scores them against a structured profile, salary floor, and remote-work requirements using the Gemini API.",
                "Built an AI tailoring pipeline that generates customized resumes, cover letters, and interview-preparation notes from job descriptions and candidate data.",
                "Hardened third-party content handling with a prompt-injection quarantine layer and SSRF protections.",
                "Tracked application history in a SQLite WAL-mode dashboard with architecture decisions documented as ADRs.",
            ],
            tags: ["Go", "Gemini API", "SQLite", "Security Hardening", "ADR Documentation"]
        }
    ],
    education: [
        {
            icon: "fa-user-graduate",
            degree: "M.S. Cyber Defense (In Progress)",
            school: "Dakota State University",
            year: ""
        },
        {
            icon: "fa-university",
            degree: "B.S. Information Technology",
            school: "Colorado State University Global Campus",
            year: ""
        },
        {
            icon: "fa-graduation-cap",
            degree: "B.B.A. Business Administration",
            school: "Rochester College",
            year: ""
        },
        {
            icon: "fa-certificate",
            degree: "Cisco Certified Network Associate (CCNA)",
            school: "Cisco Networking Academy",
            year: "2014 - 2017"
        }
    ],
    footerText: "© 2026 William Elias. All rights reserved."
};
