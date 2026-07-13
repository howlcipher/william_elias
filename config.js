const config = {
    personal: {
        name: "William Elias",
        title: "Software Engineer",
        tagline: "Python • Go • SQL • PowerShell | IT Systems & Automation | Pursuing MS Cybersecurity",
        email: "WylElias.123@gmail.com",
        phone: "586.438.6057",
        linkedin: "https://linkedin.com/in/wylelias",
        github: "https://github.com/howlcipher",
        resumePdf: "William_Elias_Resume.pdf"
    },
    summary: "Software engineer with over 9 years of experience spanning automation, web development, DevOps, QA, and production support. Specialized in Python and Go development for APIs, backend systems, and infrastructure automation. Proven ability to build secure, scalable solutions that streamline operations across development and production environments. Strong foundation in networking, security (CCNA), and system integration. Highly experienced in orchestrating zero downtime migrations, building automated security auditing tools, and managing CI/CD pipelines. Passionate about writing maintainable code and solving complex technical challenges in security focused environments.",
    skills: [
        {
            category: "Programming & Development",
            icon: "fa-code",
            tags: ["Python", "Go", "PowerShell", "SQL", "REST APIs", "ETL", "FastAPI"]
        },
        {
            category: "DevOps & Cloud",
            icon: "fa-cloud",
            tags: ["Azure DevOps", "Azure Cloud Services", "Docker", "CI/CD", "Git", "Bitbucket", "IIS"]
        },
        {
            category: "Systems & Infrastructure",
            icon: "fa-server",
            tags: ["Windows Server", "Automation Scripting", "Log Monitoring"]
        },
        {
            category: "Networking & Security",
            icon: "fa-shield-alt",
            tags: ["Cisco/Meraki", "VLANs", "Firewalls", "Packet Capture", "Monitoring"]
        },
        {
            category: "Databases",
            icon: "fa-database",
            tags: ["SQL Server", "SQLite", "Migrations", "Automated PII Masking", "Stored Procedures"]
        }
    ],
    experience: [
        {
            date: "Feb 2023 - Present",
            title: "Software Engineer (Python/Go, Automation & CI/CD)",
            company: "Stellantis Financial Services",
            location: "Auburn Hills, MI",
            achievements: [
                "Engineered a Python automation script to audit and permanently remove historical password traces and exposed credentials across over 100 Azure DevOps repositories, significantly enhancing organizational security posture.",
                "Developed a Python database transfer utility featuring automated Personally Identifiable Information (PII) masking to secure sensitive client data during migrations to lower environments.",
                "Orchestrated a massive disaster recovery cutover to new Windows servers, coordinating across Dev, IT, and DBA teams to migrate applications, firewalls, and load balancers with zero downtime.",
                "Modernized deployment workflows by creating standardized CI/CD pipeline templates for Python and .Net applications, alongside implementing UV for highly efficient Python dependency management.",
                "Designed and deployed a FastAPI Query Viewer and automated Python scripts to extract failed MuleSoft payloads, drastically reducing manual log analysis and accelerating incident resolution.",
                "Built automated file copying and service installation scripts for IIS staging environments to guarantee reliable, controlled testing for rapidly changing application builds."
            ]
        },
        {
            date: "Jul 2020 - Feb 2023",
            title: "Software Developer (Python Automation)",
            company: "HBK Engineering Solutions",
            location: "Southfield, MI",
            achievements: [
                "Designed and implemented an automated XML to database pipeline in Python, significantly improving data processing speed and accuracy.",
                "Built reusable Python libraries and internal tools to eliminate repetitive tasks for engineering teams.",
                "Developed deployment automation with validation logic to ensure secure and reliable software packaging using NSIS.",
                "Maintained version control best practices and developer tooling with Git.",
                "Provided technical support and troubleshooting for internal applications."
            ]
        },
        {
            date: "Mar 2020 - Apr 2020",
            title: "QA Developer",
            company: "Intrepid Control Systems",
            location: "Madison Heights, MI",
            achievements: [
                "Wrote and executed Mocha test cases for internal applications.",
                "Debugged and validated API alongside software and hardware integrations."
            ]
        },
        {
            date: "2015 - 2020",
            title: "Network Engineering, Security, Infrastructure",
            company: "Ford, Project Worldwide, Trendset Communications Group",
            location: "",
            achievements: [
                "Designed and deployed secure network infrastructure using Cisco/Meraki equipment.",
                "Automated network configurations and monitoring across enterprise environments.",
                "Standardized security configurations for routers, switches, and firewalls.",
                "Conducted security audits, network segmentation, and monitoring tool deployments.",
                "Provided production support for critical network and IT infrastructure."
            ]
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
