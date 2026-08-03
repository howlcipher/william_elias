const config = {
    personal: {
        name: "William Elias",
        title: "DevOps & AI Automation Engineer",
        tagline: "Platform Engineering // Python // Go // CI/CD // AI-Enabled Operations",
        location: "Michigan",
        photo: "1778619951750.jpg",
        email: "WylElias.123@gmail.com",
        phone: "586.438.6057",
        linkedin: "https://linkedin.com/in/wylelias",
        github: "https://github.com/howlcipher",
        resumePdf: "William_Elias_Resume.pdf",
        sourceRepo: "https://github.com/howlcipher/william_elias",
        sourceBranch: "main"
    },
    summary: "DevOps and automation engineer with 10+ years of experience across software delivery, infrastructure, production support, and secure engineering. Currently architecting a reusable Azure DevOps pipeline framework to scale CI/CD from one pipeline to 70+ .NET applications on IIS and building AI-enabled knowledge systems that synchronize Jira, Confluence, and SharePoint context. Combines platform engineering, hands-on operations, and AI-assisted development to eliminate repetitive work and improve reliability.",
    stats: [
        { value: "70+", label: ".NET applications in CI/CD rollout" },
        { value: "40+ hrs", label: "saved per month through automation" },
        { value: "60% / 30%", label: "processing reduction / deployment improvement" }
    ],
    skills: [
        { category: "Languages & Automation", icon: "fa-code", tags: ["Python", "Go", "C#", ".NET Framework", "PowerShell", "SQL", "REST APIs", "ETL", "XML Processing"] },
        { category: "DevOps & Platform", icon: "fa-cloud", tags: ["Azure DevOps", "YAML Templates", "CI/CD", "Git", "Bitbucket", "GitHub Actions", "IIS", "Windows Server", "Docker", "Helm", "Release Management"] },
        { category: "Cloud, Data & Security", icon: "fa-server", tags: ["Azure Monitor", "Application Insights", "Key Vault", "SQL Server", "SQLite", "Database Migrations", "Bandit SAST", "Log Monitoring"] },
        { category: "AI & Knowledge Systems", icon: "fa-robot", tags: ["Claude Code Skills", "LLM API Integration", "Multi-Agent Orchestration", "RAG", "ChromaDB", "Jira", "Confluence", "SharePoint", "Prompt Engineering"] },
        { category: "Infrastructure & Networking", icon: "fa-network-wired", tags: ["Cisco", "Meraki", "VLANs", "Firewalls", "Packet Capture", "Network Standards"] }
    ],
    experience: [
        {
            date: "Feb 2023 - Present",
            title: "Production Support Engineer - Automation, DevOps & AI Enablement",
            company: "Stellantis Financial Services",
            location: "Auburn Hills, MI",
            achievements: [
                "Independently architected a reusable Azure DevOps CI/CD framework designed to scale delivery from one pipeline to 70+ .NET applications hosted on IIS, using YAML templates, Python, PowerShell, artifact creation, deployments, and approval gates.",
                "Built and launched three new application pipelines, increasing live CI/CD coverage from one to four and replacing copy-and-paste setup that introduced human-error risk; rollout across the remaining portfolio is underway.",
                "Built an employer-owned, self-synchronizing AI knowledge library that ingests Jira, Confluence, and SharePoint content, detects stale documentation and drift, and packages Python, Go, PowerShell, Markdown context, and reusable Claude skills for global integration.",
                "Created an environment-readiness dashboard that inventories code and runtime versions plus available IIS objects across servers, enabling comparisons between environments before application promotion.",
                "Built an operations portal that centralizes scattered team links, SQL payloads for DBA approval, and service-ticket status from dependent teams in one searchable location.",
                "Developed a CI/CD-deployed, configuration-driven Python application running on a VM that is triggered by external code, queries a database, and emails results; also built Go migration utilities with recursive scanning, find/replace, and dry-run modes.",
                "Created universal IIS error pages that display error-specific guidance and prefill support emails to IT; led weekly releases and implemented database migration strategies between environments with zero data loss."
            ]
        },
        {
            date: "Jul 2020 - Feb 2023",
            title: "DevOps Engineer - Python Automation",
            company: "HBK Engineering Solutions",
            location: "Southfield, MI",
            achievements: [
                "Created a Python and Tkinter XML-output automation system that reduced data-processing time by 60%.",
                "Automated SQL output processing with Python, saving more than 40 hours per month.",
                "Developed database configuration tools that streamlined customer onboarding workflows and reduced repetitive setup.",
                "Built NSIS installer and uninstaller packages, maintained Git workflows and developer tooling, and provided live technical troubleshooting for customers."
            ]
        }
    ],
    projects: [
        { name: "Azure DevOps Pipeline Factory", subtitle: "YAML, Python, PowerShell, IIS", highlights: ["Reverse-engineered the organization's single existing pipeline into reusable templates for .NET applications, with parameterized artifact creation, IIS deployment, and approval controls.", "Launched three new pipelines and established a repeatable onboarding path for the remaining 70+ application portfolio, reducing copy-and-paste configuration and human-error risk."], tags: ["Azure DevOps", "YAML", "Python", "PowerShell", "IIS"] },
        { name: "AI Operations Knowledge Library", subtitle: "Jira, Confluence, SharePoint, Claude skills", highlights: ["Built one-way content synchronization with documentation-drift detection so stale system knowledge can be identified while current operational context remains rapidly searchable.", "Packaged reusable Claude skills and system context to support log analysis, application troubleshooting, and Jira ticket drafting or closure without repeatedly supplying background information."], tags: ["Jira", "Confluence", "SharePoint", "Claude Code", "Python", "Go"] },
        { name: "Environment Reliability Tooling", subtitle: "IIS, Python, Go, SQL", highlights: ["Created environment-comparison dashboards, centralized operations workflows, configuration-driven database reporting, migration utilities with dry-run support, and error-specific IIS support pages."], tags: ["IIS", "Python", "Go", "SQL", "Production Support"] }
    ],
    additionalExperience: [
        { company: "Intrepid Control Systems", title: "QA Developer", date: "Mar 2020 - Apr 2020", summary: "Wrote Mocha tests and debugged APIs across software and hardware integrations." },
        { company: "Project Worldwide", title: "Network Engineer", date: "Jan 2020 - Mar 2020", summary: "Configured Cisco and Meraki infrastructure and executed multi-state migrations with minimal downtime." },
        { company: "Ford Motor Company", title: "Network Standards Engineer", date: "Sep 2019 - Dec 2019", summary: "Implemented global network standards and created scalable documentation and IP-management systems." },
        { company: "Trendset Communications Group", title: "IT Network Engineer", date: "Sep 2015 - Jun 2019", summary: "Enforced network standards, maintained configuration files, and supported critical production infrastructure." }
    ],
    education: [
        { icon: "fa-user-graduate", degree: "M.S. Cyber Defense (In Progress)", school: "Dakota State University", year: "" },
        { icon: "fa-university", degree: "B.S. Information Technology", school: "Colorado State University Global Campus", year: "" },
        { icon: "fa-graduation-cap", degree: "B.B.A. Business Administration", school: "Rochester College", year: "" },
        { icon: "fa-certificate", degree: "Cisco Certified Network Associate (CCNA) - Previously held", school: "Cisco Networking Academy", year: "2014 - 2017" }
    ],
    footerText: "© 2026 William Elias. All rights reserved."
};
