import json
from pathlib import Path
from data_source_plugin_json import JsonDataSourcePlugin

test_data={
   "@id": "corp-root-28dd",
  "name": "Global Conglomerate",
  "market_cap": 5000000000.75,
  "founded_date": "1985-06-15",
  "stock_price": 156.78,
  "children": [
    {
      "@id": "div-tech-6616",
      "name": "Technology Division",
      "revenue": 800000000,
      "growth_rate": 22.5,
      "reports_to": "corp-root-28dd",
      "linked_divisions": ["div-rd-940e", "div-sales-8811", "div-ai-1234"],
      "children": [
        {
          "@id": "subdiv-software-4abc",
          "name": "Software Solutions",
          "budget": 250000000,
          "headcount": 500,
          "parent": "div-tech-6616",
          "collaborates_with": ["subdiv-hardware-5def", "team-research-9876", "team-ai-1122"],
          "children": [
            {
              "@id": "team-cloud-1a2b",
              "name": "Cloud Infrastructure",
              "project_count": 15,
              "team_size": 125,
              "parent": "subdiv-software-4abc",
              "dependencies": ["team-security-7890", "team-network-4567", "team-ai-1122"],
              "children": [
                {
                  "@id": "proj-cloud-micro",
                  "name": "Microservices Platform",
                  "status": "active",
                  "progress": 78.5,
                  "start_date": "2023-08-15",
                  "parent": "team-cloud-1a2b",
                  "related_projects": ["proj-cloud-container", "proj-security-auth", "proj-ai-ml"],
                  "team_members": ["emp-123", "emp-456", "emp-789"]
                },
                {
                  "@id": "proj-cloud-container",
                  "name": "Container Orchestration",
                  "status": "in_progress",
                  "progress": 62.3,
                  "start_date": "2023-09-01",
                  "parent": "team-cloud-1a2b",
                  "related_projects": ["proj-cloud-micro", "proj-security-auth"],
                  "team_members": ["emp-234", "emp-567", "emp-890"]
                },
                {
                  "@id": "proj-cloud-monitoring",
                  "name": "Cloud Monitoring System",
                  "status": "planning",
                  "progress": 15.0,
                  "start_date": "2024-01-15",
                  "parent": "team-cloud-1a2b",
                  "related_projects": ["proj-cloud-micro", "proj-cloud-container"],
                  "team_members": ["emp-147", "emp-258", "emp-369"]
                }
              ]
            },
            {
              "@id": "team-security-7890",
              "name": "Security Team",
              "project_count": 5,
              "team_size": 50,
              "parent": "subdiv-software-4abc",
              "dependencies": ["team-network-4567"],
              "children": [
                {
                  "@id": "proj-security-auth",
                  "name": "Authentication System",
                  "status": "active",
                  "progress": 90.0,
                  "start_date": "2023-07-01",
                  "parent": "team-security-7890",
                  "related_projects": ["proj-cloud-micro", "proj-cloud-container"],
                  "team_members": ["emp-321", "emp-654", "emp-987"]
                },
                {
                  "@id": "proj-security-encryption",
                  "name": "End-to-End Encryption",
                  "status": "in_progress",
                  "progress": 45.0,
                  "start_date": "2023-12-01",
                  "parent": "team-security-7890",
                  "related_projects": ["proj-security-auth"],
                  "team_members": ["emp-741", "emp-852", "emp-963"]
                }
              ]
            },
            {
              "@id": "team-network-4567",
              "name": "Networking Team",
              "project_count": 7,
              "team_size": 60,
              "parent": "subdiv-software-4abc",
              "dependencies": [],
              "children": [
                {
                  "@id": "proj-network-vpn",
                  "name": "VPN Infrastructure",
                  "status": "completed",
                  "progress": 100.0,
                  "start_date": "2023-06-01",
                  "parent": "team-network-4567",
                  "related_projects": ["proj-cloud-micro"],
                  "team_members": ["emp-135", "emp-246", "emp-357"]
                },
                {
                  "@id": "proj-network-sdn",
                  "name": "Software-Defined Networking",
                  "status": "active",
                  "progress": 65.0,
                  "start_date": "2023-11-01",
                  "parent": "team-network-4567",
                  "related_projects": ["proj-network-vpn", "proj-cloud-micro"],
                  "team_members": ["emp-159", "emp-267", "emp-348"]
                }
              ]
            },
            {
              "@id": "team-mobile-dev",
              "name": "Mobile Development",
              "project_count": 8,
              "team_size": 45,
              "parent": "subdiv-software-4abc",
              "dependencies": ["team-cloud-1a2b", "team-security-7890"],
              "children": [
                {
                  "@id": "proj-mobile-app",
                  "name": "Enterprise Mobile App",
                  "status": "active",
                  "progress": 55.0,
                  "start_date": "2023-10-15",
                  "parent": "team-mobile-dev",
                  "related_projects": ["proj-cloud-micro", "proj-security-auth"],
                  "team_members": ["emp-951", "emp-842", "emp-733"]
                }
              ]
            }
          ]
        },
        {
          "@id": "subdiv-hardware-5def",
          "name": "Hardware Development",
          "budget": 180000000,
          "headcount": 300,
          "parent": "div-tech-6616",
          "collaborates_with": ["subdiv-software-4abc", "team-research-9876"],
          "children": [
            {
              "@id": "team-iot-3344",
              "name": "IoT Devices",
              "project_count": 10,
              "team_size": 80,
              "parent": "subdiv-hardware-5def",
              "dependencies": ["team-cloud-1a2b", "team-ai-1122"],
              "children": [
                {
                  "@id": "proj-iot-smart-home",
                  "name": "Smart Home Solutions",
                  "status": "active",
                  "progress": 85.0,
                  "start_date": "2023-07-01",
                  "parent": "team-iot-3344",
                  "related_projects": ["proj-iot-industrial", "proj-cloud-micro"],
                  "team_members": ["emp-345", "emp-678", "emp-901"]
                },
                {
                  "@id": "proj-iot-industrial",
                  "name": "Industrial IoT Platform",
                  "status": "in_progress",
                  "progress": 40.0,
                  "start_date": "2023-11-15",
                  "parent": "team-iot-3344",
                  "related_projects": ["proj-iot-smart-home", "proj-cloud-micro"],
                  "team_members": ["emp-741", "emp-852", "emp-963"]
                }
              ]
            },
            {
              "@id": "team-embedded-5566",
              "name": "Embedded Systems",
              "project_count": 6,
              "team_size": 40,
              "parent": "subdiv-hardware-5def",
              "dependencies": ["team-iot-3344"],
              "children": [
                {
                  "@id": "proj-embedded-firmware",
                  "name": "Firmware Development",
                  "status": "active",
                  "progress": 70.0,
                  "start_date": "2023-09-15",
                  "parent": "team-embedded-5566",
                  "related_projects": ["proj-iot-smart-home", "proj-iot-industrial"],
                  "team_members": ["emp-159", "emp-267", "emp-348"]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-rd-940e",
      "name": "R&D Division",
      "budget": 600000000,
      "growth_rate": 18.7,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-tech-6616", "div-prod-3322", "div-ai-1234"],
      "children": [
        {
          "@id": "team-research-9876",
          "name": "Research Lab Alpha",
          "budget": 150000000,
          "project_count": 8,
          "parent": "div-rd-940e",
          "collaborates_with": ["subdiv-software-4abc", "team-innovation-5544", "team-ai-1122"],
          "references": ["div-tech-6616", "team-cloud-1a2b"],
          "children": [
            {
              "@id": "proj-research-ai",
              "name": "AI Initiative",
              "status": "in_progress",
              "completion": 45.7,
              "start_date": "2023-11-01",
              "parent": "team-research-9876",
              "depends_on": ["proj-cloud-micro", "div-tech-6616"]
            },
            {
              "@id": "proj-research-quantum",
              "name": "Quantum Computing",
              "status": "planning",
              "completion": 10.2,
              "start_date": "2024-02-01",
              "parent": "team-research-9876",
              "depends_on": ["proj-research-ai", "team-ai-1122"]
            }
          ]
        },
        {
          "@id": "team-innovation-5544",
          "name": "Innovation Team",
          "project_count": 6,
          "team_size": 40,
          "parent": "div-rd-940e",
          "collaborates_with": ["team-research-9876", "team-ai-1122"],
          "children": [
            {
              "@id": "proj-innovation-blockchain",
              "name": "Blockchain Research",
              "status": "in_progress",
              "progress": 30.0,
              "start_date": "2023-12-01",
              "parent": "team-innovation-5544",
              "related_projects": ["proj-research-ai"],
              "team_members": ["emp-111", "emp-222", "emp-333"]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-ai-1234",
      "name": "AI Division",
      "budget": 400000000,
      "growth_rate": 30.0,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-tech-6616", "div-rd-940e"],
      "children": [
        {
          "@id": "team-ai-1122",
          "name": "AI Research Team",
          "project_count": 12,
          "team_size": 90,
          "parent": "div-ai-1234",
          "collaborates_with": ["team-research-9876", "team-cloud-1a2b"],
          "children": [
            {
              "@id": "proj-ai-ml",
              "name": "Machine Learning Framework",
              "status": "active",
              "progress": 70.0,
              "start_date": "2023-10-01",
              "parent": "team-ai-1122",
              "related_projects": ["proj-research-ai", "proj-cloud-micro"],
              "team_members": ["emp-111", "emp-222", "emp-333"]
            },
            {
              "@id": "proj-ai-nlp",
              "name": "Natural Language Processing Engine",
              "status": "in_progress",
              "progress": 45.0,
              "start_date": "2023-11-15",
              "parent": "team-ai-1122",
              "related_projects": ["proj-ai-ml", "proj-research-ai"],
              "team_members": ["emp-444", "emp-555", "emp-666"]
            }
          ]
        },
        {
          "@id": "team-ai-applications",
          "name": "AI Applications Team",
          "project_count": 8,
          "team_size": 60,
          "parent": "div-ai-1234",
          "collaborates_with": ["team-ai-1122", "team-cloud-1a2b"],
          "children": [
            {
              "@id": "proj-ai-vision",
              "name": "Computer Vision Platform",
              "status": "active",
              "progress": 65.0,
              "start_date": "2023-09-15",
              "parent": "team-ai-applications",
              "related_projects": ["proj-ai-ml"],
              "team_members": ["emp-777", "emp-888", "emp-999"]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-sales-8811",
      "name": "Sales Division",
      "revenue": 1200000000,
      "growth_rate": 15.2,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-tech-6616", "div-marketing-7733", "div-prod-3322"],
      "children": [
        {
          "@id": "region-na-2233",
          "name": "North America",
          "revenue": 500000000,
          "team_size": 250,
          "parent": "div-sales-8811",
          "collaborates_with": ["region-eu-4455", "team-cloud-1a2b", "team-ai-1122"],
          "children": [
            {
              "@id": "team-enterprise-6677",
              "name": "Enterprise Sales",
              "revenue": 300000000,
              "deals_closed": 45,
              "parent": "region-na-2233",
              "depends_on": ["team-cloud-1a2b", "team-support-8899"],
              "references": ["proj-cloud-micro", "proj-ai-ml"]
            },
            {
              "@id": "team-support-8899",
              "name": "Customer Support",
              "team_size": 100,
              "parent": "region-na-2233",
              "collaborates_with": ["team-enterprise-6677"],
              "children": [
                {
                  "@id": "proj-support-portal",
                  "name": "Support Portal",
                  "status": "active",
                  "progress": 80.0,
                  "start_date": "2023-09-01",
                  "parent": "team-support-8899",
                  "related_projects": ["proj-cloud-micro"],
                  "team_members": ["emp-444", "emp-555", "emp-666"]
                }
              ]
            }
          ]
        },
        {
          "@id": "region-eu-4455",
          "name": "Europe",
          "revenue": 400000000,
          "team_size": 200,
          "parent": "div-sales-8811",
          "collaborates_with": ["region-na-2233", "team-ai-1122"],
          "children": [
            {
              "@id": "team-retail-9988",
              "name": "Retail Sales",
              "revenue": 250000000,
              "deals_closed": 60,
              "parent": "region-eu-4455",
              "depends_on": ["team-cloud-1a2b", "team-support-8899"],
              "references": ["proj-iot-smart-home"]
            }
          ]
        },
        {
          "@id": "region-apac-6677",
          "name": "Asia Pacific",
          "revenue": 300000000,
          "team_size": 150,
          "parent": "div-sales-8811",
          "collaborates_with": ["region-na-2233", "region-eu-4455"],
          "children": [
            {
              "@id": "team-apac-sales",
              "name": "APAC Sales Team",
              "revenue": 200000000,
              "deals_closed": 40,
              "parent": "region-apac-6677",
              "depends_on": ["team-cloud-1a2b", "team-support-8899"],
              "references": ["proj-cloud-micro", "proj-ai-ml"]
            }
          ]
        }
        
      ]
    },
    {
      "@id": "div-marketing-7733",
      "name": "Marketing Division",
      "budget": 200000000,
      "growth_rate": 10.5,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-sales-8811", "div-prod-3322"],
      "children": [
        {
          "@id": "team-digital-marketing",
          "name": "Digital Marketing",
          "budget": 80000000,
          "team_size": 40,
          "parent": "div-marketing-7733",
          "collaborates_with": ["team-enterprise-6677", "team-retail-9988"],
          "children": [
            {
              "@id": "proj-digital-campaign",
              "name": "Q1 Digital Campaign",
              "status": "active",
              "progress": 60.0,
              "start_date": "2024-01-01",
              "parent": "team-digital-marketing",
              "related_projects": ["proj-ai-ml", "proj-mobile-app"],
              "team_members": ["emp-159", "emp-267", "emp-348"]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-logistics-9900",
      "name": "Logistics Division",
      "budget": 300000000,
      "growth_rate": 8.5,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-prod-3322", "div-sales-8811"],
      "children": [
        {
          "@id": "team-supply-chain",
          "name": "Supply Chain Management",
          "budget": 150000000,
          "team_size": 75,
          "parent": "div-logistics-9900",
          "collaborates_with": ["facility-main-5544"],
          "children": [
            {
              "@id": "proj-inventory-system",
              "name": "Inventory Management System",
              "status": "in_progress",
              "progress": 40.0,
              "start_date": "2023-12-01",
              "parent": "team-supply-chain",
              "related_projects": ["proj-cloud-micro", "proj-ai-ml"],
              "team_members": ["emp-741", "emp-852", "emp-963"]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-hr-1100",
      "name": "Human Resources Division",
      "budget": 150000000,
      "growth_rate": 5.5,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-tech-6616", "div-prod-3322"],
      "children": [
        {
          "@id": "team-talent-acquisition",
          "name": "Talent Acquisition",
          "budget": 50000000,
          "team_size": 30,
          "parent": "div-hr-1100",
          "collaborates_with": ["team-ai-1122"],
          "children": [
            {
              "@id": "proj-recruitment-ai",
              "name": "AI-Powered Recruitment",
              "status": "planning",
              "progress": 20.0,
              "start_date": "2024-01-15",
              "parent": "team-talent-acquisition",
              "related_projects": ["proj-ai-ml"],
              "team_members": ["emp-951", "emp-842", "emp-733"]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-legal-1300",
      "name": "Legal Division",
      "budget": 180000000,
      "growth_rate": 4.5,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-hr-1100", "div-finance-1200"],
      "children": [
        {
          "@id": "team-compliance",
          "name": "Compliance Team",
          "budget": 70000000,
          "team_size": 25,
          "parent": "div-legal-1300",
          "collaborates_with": ["team-security-7890"],
          "children": [
            {
              "@id": "proj-compliance-automation",
              "name": "Compliance Automation System",
              "status": "in_progress",
              "progress": 35.0,
              "start_date": "2023-12-15",
              "parent": "team-compliance",
              "related_projects": ["proj-ai-ml", "proj-security-auth"],
              "team_members": ["emp-135", "emp-246", "emp-357"]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-finance-1200",
      "name": "Finance Division",
      "budget": 250000000,
      "growth_rate": 7.5,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-sales-8811", "div-prod-3322"],
      "children": [
        {
          "@id": "team-financial-planning",
          "name": "Financial Planning & Analysis",
          "budget": 100000000,
          "team_size": 45,
          "parent": "div-finance-1200",
          "collaborates_with": ["team-ai-1122"],
          "children": [
            {
              "@id": "proj-predictive-analytics",
              "name": "Predictive Financial Analytics",
              "status": "active",
              "progress": 55.0,
              "start_date": "2023-11-01",
              "parent": "team-financial-planning",
              "related_projects": ["proj-ai-ml"],
              "team_members": ["emp-321", "emp-654", "emp-987"]
            }
          ]
        }
      ]
    },
    {
      "@id": "div-prod-3322",
      "name": "Production Division",
      "revenue": 900000000,
      "growth_rate": 12.8,
      "parent": "corp-root-28dd",
      "linked_divisions": ["div-rd-940e", "div-logistics-9900", "div-sales-8811"],
      "children": [
        {
          "@id": "facility-main-5544",
          "name": "Main Factory",
          "output_capacity": 1000000,
          "efficiency_rate": 92.5,
          "parent": "div-prod-3322",
          "supplies_to": ["region-na-2233", "region-eu-4455"],
          "references": ["team-enterprise-6677", "team-retail-9988"],
          "children": [
            {
              "@id": "line-assembly-7788",
              "name": "Assembly Line A",
              "units_per_day": 5000,
              "defect_rate": 0.5,
              "parent": "facility-main-5544",
              "depends_on": ["line-parts-8899", "team-quality-1234"],
              "last_maintenance": "2024-01-15"
            },
            {
              "@id": "line-parts-8899",
              "name": "Parts Manufacturing",
              "units_per_day": 3000,
              "defect_rate": 0.3,
              "parent": "facility-main-5544",
              "depends_on": ["team-quality-1234"],
              "last_maintenance": "2024-02-01"
            }
          ]
        },
        {
          "@id": "team-quality-1234",
          "name": "Quality Assurance",
          "team_size": 50,
          "parent": "div-prod-3322",
          "collaborates_with": ["line-assembly-7788", "line-parts-8899"],
          "children": [
            {
              "@id": "proj-quality-audit",
              "name": "Quality Audit System",
              "status": "active",
              "progress": 75.0,
              "start_date": "2023-10-15",
              "parent": "team-quality-1234",
              "related_projects": ["line-assembly-7788", "line-parts-8899"],
              "team_members": ["emp-777", "emp-888", "emp-999"]
            }
          ]
        }
      ]
    },
    {
  "@id": "emp-directory",
  "name": "Employee Directory",
  "children": [
    {
      "@id": "emp-123",
      "name": "Sarah Chen",
      "role": "Senior Cloud Architect",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2020-03-15"
    },
    {
      "@id": "emp-456",
      "name": "Michael Rodriguez",
      "role": "Cloud Team Lead",
      "department": "team-cloud-1a2b",
      "reports_to": 'null',
      "hire_date": "2019-06-01"
    },
    {
      "@id": "emp-789",
      "name": "David Kim",
      "role": "Cloud DevOps Engineer",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2021-02-15"
    },
    {
      "@id": "emp-234",
      "name": "Emily Johnson",
      "role": "Container Specialist",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2021-08-01"
    },
    {
      "@id": "emp-567",
      "name": "Alex Thompson",
      "role": "Systems Engineer",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2022-01-15"
    },
    {
      "@id": "emp-890",
      "name": "Lisa Wang",
      "role": "DevOps Engineer",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2022-03-01"
    },
    {
      "@id": "emp-147",
      "name": "James Wilson",
      "role": "Monitoring Specialist",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2023-06-15"
    },
    {
      "@id": "emp-258",
      "name": "Rachel Martinez",
      "role": "SRE Engineer",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2023-07-01"
    },
    {
      "@id": "emp-369",
      "name": "Tom Anderson",
      "role": "Cloud Engineer",
      "department": "team-cloud-1a2b",
      "reports_to": "emp-456",
      "hire_date": "2023-08-15"
    },
    {
      "@id": "emp-321",
      "name": "Jennifer Lee",
      "role": "Security Lead",
      "department": "team-security-7890",
      "reports_to": 'null',
      "hire_date": "2020-01-15"
    },
    {
      "@id": "emp-654",
      "name": "Robert Taylor",
      "role": "Security Engineer",
      "department": "team-security-7890",
      "reports_to": "emp-321",
      "hire_date": "2021-04-01"
    },
    {
      "@id": "emp-987",
      "name": "Maria Garcia",
      "role": "Security Analyst",
      "department": "team-security-7890",
      "reports_to": "emp-321",
      "hire_date": "2022-02-15"
    },
    {
      "@id": "emp-741",
      "name": "Daniel Brown",
      "role": "Encryption Specialist",
      "department": "team-security-7890",
      "reports_to": "emp-321",
      "hire_date": "2023-01-15"
    },
    {
      "@id": "emp-852",
      "name": "Sophie Martin",
      "role": "Security Engineer",
      "department": "team-security-7890",
      "reports_to": "emp-321",
      "hire_date": "2023-03-01"
    },
    {
      "@id": "emp-963",
      "name": "Chris Parker",
      "role": "Security Developer",
      "department": "team-security-7890",
      "reports_to": "emp-321",
      "hire_date": "2023-04-15"
    },
    {
      "@id": "emp-135",
      "name": "Michelle White",
      "role": "Network Team Lead",
      "department": "team-network-4567",
      "reports_to": 'null',
      "hire_date": "2020-05-01"
    },
    {
      "@id": "emp-246",
      "name": "Kevin Zhang",
      "role": "Network Engineer",
      "department": "team-network-4567",
      "reports_to": "emp-135",
      "hire_date": "2021-06-15"
    },
    {
      "@id": "emp-357",
      "name": "Anna Kowalski",
      "role": "Network Security Specialist",
      "department": "team-network-4567",
      "reports_to": "emp-135",
      "hire_date": "2022-04-01"
    },
    {
      "@id": "emp-159",
      "name": "Ryan Murphy",
      "role": "SDN Engineer",
      "department": "team-network-4567",
      "reports_to": "emp-135",
      "hire_date": "2022-08-15"
    },
    {
      "@id": "emp-267",
      "name": "Laura Scott",
      "role": "Network Architect",
      "department": "team-network-4567",
      "reports_to": "emp-135",
      "hire_date": "2022-09-01"
    },
    {
      "@id": "emp-348",
      "name": "Mark Davis",
      "role": "Network Engineer",
      "department": "team-network-4567",
      "reports_to": "emp-135",
      "hire_date": "2022-10-15"
    },
    {
      "@id": "emp-951",
      "name": "Jessica Brown",
      "role": "Mobile Dev Lead",
      "department": "team-mobile-dev",
      "reports_to": 'null',
      "hire_date": "2021-01-15"
    },
    {
      "@id": "emp-842",
      "name": "Andrew Wilson",
      "role": "Senior Mobile Developer",
      "department": "team-mobile-dev",
      "reports_to": "emp-951",
      "hire_date": "2021-03-01"
    },
    {
      "@id": "emp-733",
      "name": "Nina Patel",
      "role": "Mobile Developer",
      "department": "team-mobile-dev",
      "reports_to": "emp-951",
      "hire_date": "2021-04-15"
    },
    {
      "@id": "emp-444",
      "name": "John Smith",
      "role": "Support Lead",
      "department": "team-support-8899",
      "reports_to": 'null',
      "hire_date": "2020-07-15"
    },
    {
      "@id": "emp-555",
      "name": "Amanda Jones",
      "role": "Senior Support Engineer",
      "department": "team-support-8899",
      "reports_to": "emp-444",
      "hire_date": "2021-08-01"
    },
    {
      "@id": "emp-666",
      "name": "Carlos Rivera",
      "role": "Support Engineer",
      "department": "team-support-8899",
      "reports_to": "emp-444",
      "hire_date": "2022-01-15"
    },
    {
      "@id": "emp-777",
      "name": "Patricia Chen",
      "role": "QA Lead",
      "department": "team-quality-1234",
      "reports_to": 'null',
      "hire_date": "2020-09-01"
    },
    {
      "@id": "emp-888",
      "name": "Steven Lee",
      "role": "Senior QA Engineer",
      "department": "team-quality-1234",
      "reports_to": "emp-777",
      "hire_date": "2021-10-15"
    },
    {
      "@id": "emp-999",
      "name": "Rebecca Taylor",
      "role": "QA Engineer",
      "department": "team-quality-1234",
      "reports_to": "emp-777",
      "hire_date": "2022-03-01"
    },
    {
      "@id": "emp-111",
      "name": "Alan Turing",
      "role": "AI Research Lead",
      "department": "team-ai-1122",
      "reports_to": 'null', 
      "hire_date": "2020-01-01"
    },
    {
      "@id": "emp-222",
      "name": "Grace Hopper",
      "role": "Senior AI Researcher",
      "department": "team-ai-1122",
      "reports_to": "emp-111",
      "hire_date": "2020-03-15"
    },
    {
      "@id": "emp-333",
      "name": "Ada Lovelace",
      "role": "AI Engineer",
      "department": "team-ai-1122",
      "reports_to": "emp-111",
      "hire_date": "2020-06-01"
    }
  ]
}
  ]
}
test_data_path = Path("test_data.json")
with open(test_data_path, "w", encoding="utf-8") as f:
    json.dump(test_data, f, indent=2)
plugin = JsonDataSourcePlugin()
params = {
    'file_path': str(test_data_path),
    'directed': True
}
graph = plugin.load_graph(params)
print(graph)