const config = {
    personal: {
        name: "William Elias",
        title: "DevOps Engineer",
        tagline: "Python • Go • SQL • PowerShell | Automation & CI/CD | Pursuing MS Cyber Defense",
        email: "WylElias.123@gmail.com",
        phone: "586.438.6057",
        linkedin: "https://linkedin.com/in/wylelias",
        github: "https://github.com/howlcipher",
        resumePdf: "William_Elias_Resume.pdf",
        sourceRepo: "https://github.com/howlcipher/william_elias"
    },
    summary: "Automation and systems engineer with over 10 years of experience spanning infrastructure automation, DevOps, and production support. Specialized in Python and Go development for APIs, backend systems, and automated deployment pipelines. Proven ability to build secure and scalable solutions that streamline operations across development and production environments. Strong foundation in enterprise networking, security controls, and system integration. Directs AI coding agents (Claude Code, Gemini CLI) through prompt engineering to architect, build, and test automation platforms both on the job and in personal projects. Passionate about writing maintainable code and solving complex technical challenges in security focused environments.",
    skills: [
        {
            category: "Programming & Development",
            icon: "fa-code",
            tags: ["Python", "Go", "C#", ".NET Framework", "PowerShell", "SQL", "REST APIs", "ETL"]
        },
        {
            category: "DevOps & Cloud",
            icon: "fa-cloud",
            tags: ["Azure DevOps", "Application Insights", "Key Vault", "Azure Monitor", "CI/CD", "Git", "Bitbucket", "IIS"]
        },
        {
            category: "Systems & Infrastructure",
            icon: "fa-server",
            tags: ["Windows Server", "Automation Scripting", "Log Monitoring", "Job Scheduling"]
        },
        {
            category: "Networking & Security",
            icon: "fa-shield-alt",
            tags: ["Cisco/Meraki", "VLANs", "Firewalls", "Packet Capture", "Monitoring Tools"]
        },
        {
            category: "Databases",
            icon: "fa-database",
            tags: ["SQL Server", "SQLite", "Migrations", "Stored Procedures", "Reporting"]
        },
        {
            category: "AI & Automation",
            icon: "fa-robot",
            tags: ["AI-Augmented Development", "Prompt Engineering", "Claude Code", "Gemini CLI", "LLM API Integration", "ChromaDB / RAG"]
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
                "Built custom tools with Go and PowerShell, successfully streamlining deployment processes by 30 percent.",
                "Implemented database migration strategies between environments with zero data loss.",
                "Managed IIS applications including configuration, troubleshooting, and performance optimization.",
                "Led weekly releases and deployments using Git workflows and Bitbucket.",
                "Built backend scripts for log parsing, anomaly detection, and data validation to support production operations.",
                "Built an internal documentation and issue-discovery platform with Claude Code that polls Jira and SharePoint across the team, flags drift between documentation and production state, and lets new employees ask questions in plain language to speed up onboarding and production troubleshooting.",
                "Built a production support portal centralizing team links, runbooks, and documentation into a single searchable hub, reducing time spent hunting for operational resources."
            ]
        },
        {
            date: "Jul 2020 - Feb 2023",
            title: "DevOps Engineer (Python Automation)",
            company: "HBK Engineering Solutions",
            location: "Southfield, MI",
            achievements: [
                "Created an XML output automation system with Python and Tkinter, reducing data processing time by 60 percent.",
                "Automated SQL output processing with Python scripts, saving over 40 hours monthly.",
                "Developed custom database configuration tools that streamlined customer onboarding workflows.",
                "Built installer and uninstaller packages using NSIS scripting for seamless application deployment.",
                "Maintained version control best practices and developer tooling with Git.",
                "Provided direct technical support to customers through live interactive troubleshooting sessions."
            ]
        },
        {
            date: "Mar 2020 - Apr 2020",
            title: "QA Developer",
            company: "Intrepid Control Systems",
            location: "Madison Heights, MI",
            achievements: [
                "Wrote and executed Mocha test cases for internal software applications.",
                "Debugged and validated API alongside software and hardware integrations."
            ]
        },
        {
            date: "Jan 2020 - Mar 2020",
            title: "Network Engineer",
            company: "Project Worldwide",
            location: "",
            achievements: [
                "Configured Cisco switches and Meraki access points across multiple enterprise company locations.",
                "Developed comprehensive network documentation standards including specific IP addressing schemes.",
                "Executed multi state network migration projects with minimal operational downtime."
            ]
        },
        {
            date: "Sep 2019 - Dec 2019",
            title: "Network Standards Engineer",
            company: "Ford Motor Company",
            location: "",
            achievements: [
                "Implemented global network configuration standards across distributed enterprise infrastructure.",
                "Created documentation templates and IP management databases to scale organizational efficiency.",
                "Supported large scale network migrations with comprehensive planning and technical execution."
            ]
        },
        {
            date: "Sep 2015 - Jun 2019",
            title: "IT Network Engineer",
            company: "Trendset Communications Group",
            location: "",
            achievements: [
                "Enforced strict network standards and performed comprehensive audits covering ports, IPs, and VLANs.",
                "Maintained complex configuration files for diverse network equipment environments.",
                "Provided tier production support for critical network infrastructure and organizational uptime."
            ]
        }
    ],
    projects: [
        {
            name: "AI Knowledge Library",
            subtitle: "Multi-agent orchestration platform - Python, Go",
            highlights: [
                "Directed AI coding agents (Claude Code, Gemini CLI) through prompt engineering to design, implement, and test a platform that routes engineering work across multiple AI providers (Claude, Gemini, local Ollama models) with shared skills, rules, and project context.",
                "Built a skill-routing system with keyword and ChromaDB semantic-search fallback to automatically surface relevant domain knowledge into AI agent sessions.",
                "Enforced production-grade quality with a 148-test Python and Go suite, bandit SAST scanning, and pre-push CI gates that block unverified code from shipping.",
                "Packaged as a Go-built CLI installer with a Helm chart and Docker/GitHub Actions deployment.",
            ],
            tags: ["Python", "Go", "Claude Code", "Gemini CLI", "ChromaDB", "Helm", "Docker", "GitHub Actions"]
        },
        {
            name: "Career Agent Core",
            subtitle: "AI-powered job search assistant - Go",
            highlights: [
                "Directed AI coding agents (Claude Code, Gemini CLI) through prompt engineering to architect and build a Go service that aggregates remote job postings and scores them against a structured profile, salary floor, and remote-work requirements using the Gemini API.",
                "Built an AI tailoring pipeline that synthesizes job descriptions against a candidate profile to generate customized resumes, cover letters, and interview prep notes.",
                "Hardened the system against untrusted third-party content with a prompt-injection quarantine layer and SSRF protections.",
                "Tracked application history in a SQLite-backed dashboard (WAL mode) with architecture decisions documented as ADRs.",
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
