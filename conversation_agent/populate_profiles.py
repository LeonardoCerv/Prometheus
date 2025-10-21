#!/usr/bin/env python3
"""
Script to populate Firebase Firestore with sample professional profiles
"""
import os
import sys
import random
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Sample data pools
FIRST_NAMES = [
    "Ana", "Carlos", "María", "José", "Isabel", "Antonio", "Carmen", "Francisco",
    "Pilar", "Juan", "Teresa", "Miguel", "Cristina", "David", "Lucía", "Alejandro",
    "Mónica", "Rafael", "Elena", "Pablo", "Silvia", "Diego", "Patricia", "Javier",
    "Rosa", "Luis", "Dolores", "Fernando", "Mercedes", "Sergio", "Raquel", "Alberto",
    "Concepción", "Roberto", "Manuela", "Adrián", "Beatriz", "Rubén", "Inés", "Óscar"
]

LAST_NAMES = [
    "García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez",
    "Martín", "Ruiz", "Hernández", "Jiménez", "Díaz", "Moreno", "Álvarez", "Muñoz",
    "Romero", "Navarro", "Torres", "Ramírez", "Gil", "Vargas", "Serrano", "Blanco",
    "Molina", "Morales", "Ortega", "Delgado", "Castro", "Ortiz", "Rubio", "Sanz",
    "Iglesias", "Cortés", "Gutiérrez", "Castillo", "Guerrero", "Domínguez", "Vega", "Flores"
]

CITIES = [
    "Madrid, España", "Barcelona, España", "Valencia, España", "Sevilla, España", "Zaragoza, España",
    "Málaga, España", "Murcia, España", "Palma de Mallorca, España", "Las Palmas de Gran Canaria, España", "Bilbao, España",
    "Buenos Aires, Argentina", "México DF, México", "Santiago, Chile", "Bogotá, Colombia", "Lima, Perú",
    "Caracas, Venezuela", "Quito, Ecuador", "Montevideo, Uruguay", "Asunción, Paraguay", "La Paz, Bolivia"
]

# Tech skills organized by category
FRONTEND_SKILLS = [
    "React", "Vue.js", "Angular", "Next.js", "TypeScript", "JavaScript", "HTML5",
    "CSS3", "Tailwind CSS", "SASS", "Redux", "MobX", "Webpack", "Vite", "GraphQL"
]

BACKEND_SKILLS = [
    "Node.js", "Python", "Django", "Flask", "FastAPI", "Express.js", "Java",
    "Spring Boot", "Ruby on Rails", "Go", "Rust", "C#", ".NET", "PHP", "Laravel"
]

DATABASE_SKILLS = [
    "PostgreSQL", "MongoDB", "MySQL", "Redis", "Firebase", "Firestore",
    "DynamoDB", "Cassandra", "Neo4j", "ElasticSearch", "SQL Server"
]

CLOUD_DEVOPS = [
    "AWS", "Google Cloud", "Azure", "Docker", "Kubernetes", "CI/CD", "Jenkins",
    "GitHub Actions", "Terraform", "Ansible", "Linux", "Nginx", "Apache"
]

DATA_AI = [
    "Machine Learning", "TensorFlow", "PyTorch", "scikit-learn", "Pandas",
    "NumPy", "Data Analysis", "SQL", "R", "Jupyter", "Power BI", "Tableau"
]

MOBILE = [
    "React Native", "Flutter", "Swift", "iOS", "Android", "Kotlin", "Xamarin"
]

OTHER_SKILLS = [
    "Git", "Agile", "Scrum", "REST APIs", "Microservices", "Testing",
    "Jest", "Pytest", "Cypress", "Selenium", "Security", "OAuth"
]

JOB_TITLES = [
    "Ingeniero de Software", "Desarrollador Full Stack", "Desarrollador Frontend", "Desarrollador Backend",
    "Ingeniero de Software Senior", "Desarrollador Líder", "Ingeniero DevOps", "Científico de Datos",
    "Ingeniero de Machine Learning", "Desarrollador Móvil", "Ingeniero UI/UX", "Líder Técnico",
    "Arquitecto de Soluciones", "Ingeniero de la Nube", "Ingeniero de Plataformas"
]

COMPANIES = [
    "Google", "Meta", "Amazon", "Microsoft", "Apple", "Netflix", "Airbnb", "Uber",
    "Lyft", "Twitter", "LinkedIn", "Salesforce", "Adobe", "Oracle", "IBM",
    "Shopify", "Stripe", "Spotify", "Dropbox", "Slack", "Zoom", "Atlassian",
    "GitHub", "GitLab", "Red Hat", "VMware", "Cisco", "Intel", "NVIDIA",
    "Indra", "Telefónica", "BBVA", "Santander", "Iberdrola", "Repsol", "Endesa",
    "Mercadona", "El Corte Inglés", "Inditex", "Accenture", "Deloitte", "PwC"
]

UNIVERSITIES = [
    "Universidad Complutense de Madrid", "Universidad de Barcelona", "Universidad Autónoma de Madrid", "Universidad Politécnica de Madrid",
    "Universidad de Valencia", "Universidad de Sevilla", "Universidad Autónoma de Barcelona", "Universidad Carlos III de Madrid",
    "Universidad Pompeu Fabra", "Universidad de Granada", "Universidad de Zaragoza", "Universidad de Salamanca",
    "Universidad de Valladolid", "Universidad de Córdoba", "Universidad de Málaga", "Universidad de Alicante",
    "Universidad de Murcia", "Universidad de La Laguna", "Universidad de Las Palmas de Gran Canaria", "Universidad de Santiago de Compostela"
]

DEGREES = [
    "Ingeniería Informática", "Desarrollo de Software", "Sistemas de Información",
    "Ingeniería de Computadores", "Ciencia de Datos", "Ingeniería Eléctrica", "Matemáticas",
    "Estadística", "Inteligencia Artificial", "Ciberseguridad"
]

PROJECT_TYPES = [
    "Plataforma de Comercio Electrónico", "Aplicación de Redes Sociales", "Dashboard de Analytics", "Aplicación Móvil",
    "Servicio API", "Chat en Tiempo Real", "Streaming de Video", "Pasarela de Pagos",
    "Chatbot con IA", "Plataforma IoT", "Migración a la Nube", "Arquitectura de Microservicios",
    "Sistema de Gestión Empresarial", "Aplicación de Gestión de Tareas", "Plataforma Educativa",
    "Sistema de Recomendaciones", "Aplicación de Salud", "Plataforma de Fintech"
]

CERTIFICATIONS = [
    "AWS Certified Solutions Architect", "Google Cloud Professional Cloud Architect", "Microsoft Azure Solutions Architect",
    "Certified Kubernetes Administrator", "Docker Certified Associate", "Certified Scrum Master",
    "PMI Project Management Professional", "Cisco Certified Network Associate", "CompTIA Security+",
    "Oracle Certified Java Programmer", "MongoDB Certified Developer", "TensorFlow Developer Certificate"
]

LANGUAGES = [
    "Español (Nativo)", "Inglés (Fluido)", "Francés (Intermedio)", "Alemán (Básico)", "Portugués (Intermedio)",
    "Italiano (Básico)", "Chino Mandarín (Básico)", "Japonés (Básico)"
]

INTERESTS = [
    "Inteligencia Artificial", "Machine Learning", "Desarrollo Sostenible", "Blockchain", "Realidad Virtual",
    "Ciberseguridad", "Automatización", "Análisis de Datos", "Desarrollo Móvil", "Computación en la Nube",
    "Open Source", "Mentoría", "Innovación Tecnológica", "Deportes Electrónicos", "Fotografía Digital"
]


def generate_profile():
    """Generate a realistic professional profile"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    phone = f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    location = random.choice(CITIES)
    
    # Generate profile image URL (leave blank to use default avatar)
    profile_image = ""
    
    # Build skills list - randomly sampled from all categories for maximum flexibility
    skills = []
    # Random sampling from each skill category with varying amounts
    skills.extend(random.sample(FRONTEND_SKILLS, random.randint(2, min(8, len(FRONTEND_SKILLS)))))
    skills.extend(random.sample(BACKEND_SKILLS, random.randint(2, min(8, len(BACKEND_SKILLS)))))
    skills.extend(random.sample(DATABASE_SKILLS, random.randint(1, min(6, len(DATABASE_SKILLS)))))
    skills.extend(random.sample(CLOUD_DEVOPS, random.randint(1, min(6, len(CLOUD_DEVOPS)))))
    skills.extend(random.sample(OTHER_SKILLS, random.randint(2, min(7, len(OTHER_SKILLS)))))
    skills.extend(random.sample(DATA_AI, random.randint(0, min(5, len(DATA_AI)))))
    skills.extend(random.sample(MOBILE, random.randint(0, min(5, len(MOBILE)))))
    skills = list(set(skills))  # Remove duplicates
    random.shuffle(skills)
    
    # Generate job experience (highly variable based on experience)
    years_of_experience = random.randint(0, 15)  # From recent graduate to senior
    num_jobs = random.randint(0, min(6, max(1, years_of_experience + random.randint(-1, 2))))  # Very flexible
    job_experience = []
    
    current_year = datetime.now().year
    for i in range(num_jobs):
        years_in_job = random.randint(1, 3) if i > 0 else max(1, years_of_experience % 3 or 1)
        end_year = current_year - sum([random.randint(1, 3) for _ in range(i)])  # Varied job lengths
        start_year = end_year - years_in_job
        
        title = random.choice(JOB_TITLES)  # All jobs get titles from the full list
        
        company = random.choice(COMPANIES)
        
        # Generate extensive responsibilities (8-12 instead of 5)
        responsibilities = [
            f"Desarrollé y mantuve {random.choice(['aplicaciones web complejas', 'apps móviles nativas', 'servicios backend escalables', 'pipelines de datos automatizados', 'sistemas de microservicios', 'APIs RESTful de alto rendimiento'])} utilizando {random.choice(skills[:3])} y {random.choice(skills[3:6])}",
            f"Colaboré con equipos multifuncionales de {random.randint(5, 15)} personas para entregar {random.choice(['características innovadoras', 'productos de software complejos', 'soluciones empresariales', 'servicios críticos para el negocio', 'plataformas SaaS'])} bajo metodologías ágiles",
            f"Mejoré significativamente {random.choice(['el rendimiento del sistema', 'la escalabilidad de la arquitectura', 'la experiencia del usuario final', 'la calidad y mantenibilidad del código', 'la eficiencia de los procesos de desarrollo'])} en un {random.randint(30, 90)}%, implementando optimizaciones avanzadas",
            f"Lideré la implementación de nuevas tecnologías emergentes como {random.choice(['arquitecturas serverless', 'contenedores Docker', 'orquestación Kubernetes', 'bases de datos NoSQL', 'frameworks de machine learning', 'soluciones de cloud computing'])} y mejores prácticas de desarrollo",
            f"Participé activamente en revisiones de código, mentoría de {random.randint(2, 5)} desarrolladores junior, y contribuí a la definición de estándares de codificación y procesos de CI/CD",
            f"Realicé análisis de rendimiento y optimización de consultas de base de datos, reduciendo los tiempos de respuesta de {random.randint(40, 80)}% y mejorando la eficiencia general del sistema",
            f"Implementé soluciones de monitoreo y logging avanzadas utilizando herramientas como {random.choice(['ELK Stack', 'Prometheus + Grafana', 'DataDog', 'New Relic', 'Splunk'])} para asegurar la estabilidad y observabilidad de las aplicaciones",
            f"Colaboré en la migración de sistemas legacy a arquitecturas modernas, modernizando {random.randint(3, 8)} aplicaciones críticas y reduciendo costos operativos en un {random.randint(25, 60)}%",
            f"Desarrollé y mantuve suites de testing automatizados, logrando cobertura de código superior al {random.randint(80, 95)}% y reduciendo bugs en producción en un {random.randint(50, 80)}%",
            f"Participé en la planificación estratégica de productos, contribuyendo al diseño de roadmaps técnicos y estimaciones de esfuerzo para proyectos de {random.randint(6, 24)} meses de duración"
        ]
        
        # Randomly select 8-12 responsibilities for each job
        selected_responsibilities = random.sample(responsibilities, random.randint(8, min(12, len(responsibilities))))
        
        job_experience.append({
            "role": title,
            "company": company,
            "startDate": f"{start_year}-{random.randint(1, 12):02d}",
            "endDate": f"{end_year}-{random.randint(1, 12):02d}" if i > 0 else "Present",
            "responsibilities": selected_responsibilities,
            "achievements": f"Logré {random.choice(['incrementar la productividad del equipo', 'reducir costos operativos', 'mejorar métricas de usuario', 'acelerar tiempos de entrega'])} en un {random.randint(25, 70)}% durante mi permanencia"
        })
    
    # Generate education (more extensive with additional details)
    university = random.choice(UNIVERSITIES)
    degree = random.choice(DEGREES)
    grad_year = current_year - years_of_experience - random.randint(0, 3)
    
    # Generate relevant coursework
    all_coursework = [
        "Algoritmos y Estructuras de Datos", "Bases de Datos", "Sistemas Operativos", "Redes de Computadoras",
        "Ingeniería de Software", "Programación Orientada a Objetos", "Análisis y Diseño de Sistemas",
        "Inteligencia Artificial", "Machine Learning", "Ciencia de Datos", "Desarrollo Web", "Aplicaciones Móviles",
        "Seguridad Informática", "Arquitectura de Software", "DevOps y Cloud Computing", "Matemáticas Discretas",
        "Estadística", "Probabilidad", "Cálculo", "Física", "Electrónica Digital"
    ]
    coursework = random.sample(all_coursework, min(random.randint(8, 12), len(all_coursework)))
    
    education = [{
        "degree": f"Licenciatura en {degree}",
        "institution": university,
        "graduationDate": f"{grad_year}",
        "gpa": round(random.uniform(3.3, 4.0), 2),
        "honors": random.choice([None, "Mención Honorífica", "Cum Laude", "Magna Cum Laude"]) if random.random() > 0.6 else None,
        "thesis": f"Tesis: {random.choice(['Desarrollo de un sistema de recomendación inteligente', 'Optimización de algoritmos de machine learning', 'Arquitectura de microservicios escalables', 'Análisis de big data para predicción de tendencias', 'Sistema de seguridad blockchain', 'Aplicación móvil para gestión educativa'])}" if random.random() > 0.7 else None,
        "relevant_coursework": coursework,
        "activities": random.sample([
            "Club de Programación", "Sociedad de Estudiantes de Ingeniería", "Proyecto de Investigación",
            "Equipo de Robótica", "Hackathon Anual", "Mentoría de Estudiantes", "Proyecto de Software Libre"
        ], min(random.randint(1, 3), 7)) if random.random() > 0.5 else []
    }]
    
    # Add master's degree (random chance based on experience)
    if random.random() > max(0.1, 0.6 - years_of_experience * 0.03):  # Higher chance with more experience, but still random
        master_degree = random.choice(DEGREES)
        master_university = random.choice(UNIVERSITIES)
        master_coursework = random.sample([
            "Arquitectura de Software Avanzada", "Machine Learning Avanzado", "Sistemas Distribuidos",
            "Investigación en Computación", "Gestión de Proyectos de Software", "Seguridad de Sistemas",
            "Computación en la Nube", "Big Data Analytics", "Inteligencia Artificial", "Blockchain",
            "DevOps Avanzado", "Ingeniería de Datos", "Ciberseguridad", "Computación Móvil"
        ], min(random.randint(4, 12), 14))
        
        education.insert(0, {
            "degree": f"Maestría en {master_degree}",
            "institution": master_university,
            "graduationDate": f"{grad_year + random.randint(1, 3)}",
            "gpa": round(random.uniform(3.5, 4.0), 2),
            "honors": random.choice([None, "Mención Honorífica", "Cum Laude"]) if random.random() > 0.7 else None,
            "thesis": f"Tesis de Maestría: {random.choice(['Modelo predictivo para optimización de recursos cloud', 'Sistema de detección de anomalías en tiempo real', 'Arquitectura de datos para aplicaciones IoT', 'Algoritmos de optimización para sistemas distribuidos', 'Plataforma de análisis de sentimientos en redes sociales', 'Sistema de recomendación basado en grafos'])}" if random.random() > 0.8 else None,
            "relevant_coursework": master_coursework,
            "specialization": random.choice([
                "Inteligencia Artificial y Machine Learning", "Arquitectura de Software Empresarial",
                "Ciberseguridad y Protección de Datos", "Computación en la Nube", "Big Data e Analytics",
                "Desarrollo de Software Avanzado", "Sistemas Distribuidos", "Computación Móvil"
            ]),
            "activities": random.sample([
                "Grupo de Investigación", "Publicación en Conferencias", "Proyecto de Investigación Aplicada",
                "Colaboración con Industria", "Desarrollo de Software de Código Abierto"
            ], min(random.randint(0, 3), 5)) if random.random() > 0.6 else []
        })
    
    # Add PhD (very random, rare)
    if random.random() > max(0.05, 0.85 - years_of_experience * 0.02):  # Very low chance, increases slightly with experience
        phd_university = random.choice(UNIVERSITIES)
        phd_topic = random.choice([
            "Inteligencia Artificial aplicada a la optimización de sistemas", 
            "Arquitecturas de software para sistemas de alta disponibilidad",
            "Algoritmos de machine learning para procesamiento de big data",
            "Seguridad en sistemas distribuidos y blockchain",
            "Computación en la nube y virtualización avanzada"
        ])
        
        education.insert(0, {
            "degree": "Doctorado en Informática",
            "institution": phd_university,
            "graduationDate": f"{grad_year + random.randint(3, 6)}",
            "thesis": f"Tesis Doctoral: {phd_topic}",
            "publications": random.sample([
                "Artículo en revista internacional JCR", "Conferencia internacional IEEE",
                "Capítulo de libro académico", "Patente de software", "Proyecto de investigación financiado"
            ], min(random.randint(1, 6), 5)),
            "research_focus": phd_topic,
            "supervisor": f"Dr. {random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        })
    
    # Generate projects (highly variable)
    num_projects = random.randint(0, min(8, years_of_experience + random.randint(0, 3)))
    projects = []
    for _ in range(num_projects):
        project_type = random.choice(PROJECT_TYPES)
        tech_stack = random.sample(skills, min(8, len(skills)))  # Increased from 4
        
        # Generate more extensive project descriptions
        project_descriptions = [
            f"Construí una {project_type.lower()} escalable y robusta desde cero, sirviendo actualmente a más de {random.randint(5000, 100000)} usuarios activos mensuales. Implementé características avanzadas como autenticación OAuth2, procesamiento de pagos integrado, notificaciones push, y un dashboard administrativo completo. El sistema maneja {random.randint(100000, 1000000)} transacciones diarias con un tiempo de respuesta promedio de {random.randint(50, 150)}ms. Utilicé {', '.join(tech_stack[:4])} en el frontend y {', '.join(tech_stack[4:8])} en el backend, implementando mejores prácticas como TDD, CI/CD, y monitoreo continuo. El proyecto resultó en {random.choice(['un crecimiento del 300% en usuarios', 'reducción del 60% en costos operativos', 'incremento del 80% en satisfacción del cliente', 'expansión a 5 países adicionales'])}.",
            
            f"Desarrollé una plataforma {project_type.lower()} innovadora que revolucionó el sector, procesando {random.randint(1000000, 10000000)} de datos diariamente. La arquitectura incluye microservicios desacoplados, bases de datos distribuidas, y un sistema de cache multinivel. Implementé algoritmos de machine learning para recomendaciones personalizadas, logrando una precisión del {random.randint(85, 95)}%. El stack tecnológico incluyó {', '.join(tech_stack[:6])}, con énfasis en escalabilidad y mantenibilidad. El proyecto recibió {random.choice(['reconocimiento internacional', 'premio a la innovación', 'financiamiento de serie A', 'adopción por empresas Fortune 500'])} y actualmente genera {random.randint(50000, 500000)} USD mensuales.",
            
            f"Lideré el desarrollo de un sistema {project_type.lower()} de nivel empresarial que maneja operaciones críticas para {random.randint(50, 500)} clientes corporativos. La solución incluye APIs RESTful documentadas, integración con sistemas legacy, y un portal de administración intuitivo. Implementé características avanzadas como analítica en tiempo real, reportes automatizados, y integración con {random.randint(10, 30)} servicios externos. Utilizando {', '.join(tech_stack[:5])}, logré una disponibilidad del 99.9% y tiempos de respuesta inferiores a {random.randint(100, 300)}ms. El proyecto resultó en {random.choice(['ahorro de 2M USD anuales', 'incremento del 150% en eficiencia operativa', 'reducción del 70% en errores manuales', 'expansión internacional'])} para los clientes.",
            
            f"Creé una aplicación {project_type.lower()} de vanguardia que combina tecnologías emergentes con interfaces de usuario innovadoras. El sistema procesa {random.randint(10000, 100000)} solicitudes concurrentes, utilizando algoritmos de optimización avanzados y aprendizaje automático. Implementé un sistema de recomendaciones inteligente que mejora la experiencia del usuario en un {random.randint(40, 80)}%. El stack incluyó {', '.join(tech_stack[:7])}, con énfasis en performance y seguridad. El proyecto fue {random.choice(['adoptado por startups unicornio', 'presentado en conferencias internacionales', 'patentado parcialmente', 'escalado a nivel global'])} y actualmente soporta {random.randint(100000, 1000000)} usuarios activos.",
            
            f"Desarrollé una plataforma {project_type.lower()} completa que integra múltiples sistemas heterogéneos, proporcionando una experiencia unificada para usuarios finales. La arquitectura incluye {random.randint(15, 40)} microservicios, bases de datos NoSQL y SQL, y un sistema de mensajería asíncrona. Implementé funcionalidades avanzadas como búsqueda full-text, filtros inteligentes, y exportación de datos en múltiples formatos. Utilizando {', '.join(tech_stack[:6])}, logré una escalabilidad horizontal y tolerancia a fallos. El proyecto generó {random.choice(['ingresos recurrentes de 200K USD/mes', 'reducción del 50% en tiempo de desarrollo', 'incremento del 300% en engagement de usuarios', 'adopción por el 80% del mercado objetivo'])}."
        ]
        
        selected_description = random.choice(project_descriptions)
        
        # Generate additional project details
        project_role = random.choice([
            "Desarrollador Principal", "Arquitecto de Software", "Líder Técnico", 
            "Desarrollador Full Stack", "Ingeniero Backend", "Ingeniero Frontend",
            "DevOps Engineer", "Data Engineer", "Product Owner Técnico"
        ])
        
        team_size = random.randint(3, 15)
        duration_months = random.randint(3, 18)
        
        projects.append({
            "name": f"{project_type}",
            "description": selected_description,
            "technologies": tech_stack,
            "role": project_role,
            "team_size": team_size,
            "duration_months": duration_months,
            "link": f"https://github.com/{first_name.lower()}{last_name.lower()}/{project_type.lower().replace(' ', '-')}",
            "metrics": {
                "users": random.randint(1000, 1000000),
                "performance": f"{random.randint(50, 200)}ms respuesta promedio",
                "uptime": f"{random.randint(99, 100)}.{random.randint(5, 9)}% disponibilidad",
                "scale": f"{random.choice(['10K', '100K', '1M', '10M'])} requests/día"
            },
            "challenges": random.sample([
                "Escalabilidad a alto volumen de usuarios", "Integración con sistemas legacy",
                "Optimización de performance crítica", "Implementación de seguridad avanzada",
                "Migración de arquitectura monolítica a microservicios", "Implementación de CI/CD",
                "Gestión de datos sensibles y compliance", "Desarrollo de APIs públicas"
            ], min(random.randint(2, 4), 8))
        })
    
    # Generate certifications (highly variable)
    num_certifications = random.randint(0, min(10, years_of_experience + random.randint(0, 4)))
    certifications = random.sample(CERTIFICATIONS, num_certifications) if num_certifications > 0 else []
    
    # Add certification details
    certifications_with_details = []
    for cert in certifications:
        cert_year = current_year - random.randint(0, 3)
        issuing_org = "Amazon Web Services" if "AWS" in cert else \
                     "Google Cloud" if "Google" in cert else \
                     "Microsoft" if "Microsoft" in cert else \
                     "Certificación Profesional"
        
        certifications_with_details.append({
            "name": cert,
            "issuing_organization": issuing_org,
            "issue_date": f"{cert_year}",
            "expiration_date": f"{cert_year + random.randint(2, 3)}" if random.random() > 0.5 else None,
            "credential_id": f"CERT-{random.randint(100000, 999999)}"
        })
    
    # Generate languages (highly variable)
    num_languages = random.randint(1, 5)
    base_languages = random.sample(LANGUAGES, min(num_languages, len(LANGUAGES)))
    languages = []
    for lang in base_languages:
        proficiency_levels = ["Básico", "Intermedio", "Avanzado", "Nativo", "Fluido"]
        if "Nativo" in lang:
            level = "Nativo"
        elif "Fluido" in lang:
            level = "Fluido"
        else:
            level = random.choice(proficiency_levels)
        
        languages.append(f"{lang.split(' (')[0]} ({level})")
    
    # Generate interests (highly variable)
    additional_interests = [
        "Desarrollo de videojuegos indie", "Contribución a proyectos open source", "Mentoría técnica",
        "Escritura técnica y blogging", "Participación en comunidades de desarrollo", "Investigación académica",
        "Emprendimiento tecnológico", "Inversión en startups", "Fotografía digital", "Producción musical",
        "Deportes extremos", "Viajes culturales", "Gastronomía internacional", "Literatura de ciencia ficción",
        "Arte digital", "Música electrónica", "Fotografía de naturaleza", "Cocina experimental"
    ]
    
    all_interests = INTERESTS + additional_interests
    num_interests = random.randint(2, min(12, len(all_interests)))
    interests = random.sample(all_interests, num_interests)
    
    # Build extensive bio (highly variable structure)
    if years_of_experience < 3:
        bio_titles = ["Software Developer", "Junior Developer", "Full Stack Developer", "Web Developer", "Desarrollador de Software"]
    else:
        bio_titles = ["Senior Software Engineer", "Full Stack Developer", "Software Architect", "Tech Lead", "Principal Engineer", "Ingeniero Senior", "Arquitecto de Software"]
    bio_title = random.choice(bio_titles)
    
    bio_parts = [
        f"{name} es un {bio_title}",
        f"{'recién graduado' if years_of_experience < 1 else f'con {years_of_experience} años de experiencia'} en el desarrollo de software.",
        f" Actualmente {'trabaja' if job_experience else 'busca oportunidades'} como {job_experience[0]['role'] if job_experience else 'desarrollador'} {'en ' + job_experience[0]['company'] if job_experience else ''}.",
        f" Se especializa en {random.choice(['tecnologías modernas', 'desarrollo full-stack', 'soluciones innovadoras', 'arquitecturas escalables'])} incluyendo {', '.join(random.sample(skills, min(3, len(skills))))}.",
        f" Su formación académica incluye {education[0]['degree']} de {education[0]['institution']}, complementada con {len(certifications_with_details)} certificaciones profesionales.",
    ]
    
    if projects:
        bio_parts.append(f" Ha {'desarrollado' if len(projects) < 3 else 'liderado'} {len(projects)} proyectos tecnológicos que han impactado a miles de usuarios.")
    
    bio_parts.extend([
        f" Domina {len(languages)} idiomas y mantiene intereses en {', '.join(random.sample(interests, min(3, len(interests))))}.",
        f" Apasionado por {'la innovación tecnológica' if random.random() > 0.5 else 'el aprendizaje continuo'}, busca proyectos desafiantes que generen impacto real."
    ])
    
    bio = "".join(bio_parts)
    
    # Create the profile data structure matching Firebase schema
    profile_data = {
        "personal_info": {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "image": profile_image
        },
        "job_experience": job_experience,
        "education": education,
        "skills": ", ".join(skills),  # Skills as comma-separated string
        "projects": projects,
        "certifications": certifications_with_details,
        "languages": languages,
        "interests": interests
    }
    
    # Top-level fields
    return {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phone": phone,
        "location": location,
        "profession": bio_title,
        "profileData": profile_data,
        "createdAt": firestore.SERVER_TIMESTAMP,
        "updatedAt": firestore.SERVER_TIMESTAMP
    }


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        firebase_admin.get_app()
        print("✅ Firebase already initialized")
    except ValueError:
        # Try to find the service account key
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "my_agent", "serviceAccount.json"),
            os.path.join(os.path.dirname(__file__), "serviceAccount.json"),
            os.path.join(os.path.dirname(__file__), "serviceAccountKey.json"),
            os.path.join(os.path.dirname(__file__), "..", "serviceAccountKey.json"),
            "serviceAccountKey.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"🔑 Using service account key: {path}")
                cred = credentials.Certificate(path)
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized successfully")
                return
        
        print("❌ Error: serviceAccount.json not found!")
        print("Please place your Firebase service account key in one of these locations:")
        for path in possible_paths:
            print(f"  - {os.path.abspath(path)}")
        sys.exit(1)


def populate_database(num_profiles=50):
    """Populate Firebase with sample profiles"""
    print("\n" + "="*80)
    print(f"🚀 POPULATING DATABASE WITH {num_profiles} PROFILES")
    print("="*80 + "\n")
    
    initialize_firebase()
    db = firestore.client()
    
    collection_ref = db.collection('userProfiles')
    
    success_count = 0
    for i in range(num_profiles):
        try:
            profile = generate_profile()
            doc_ref = collection_ref.document()
            doc_ref.set(profile)
            
            name = profile['profileData']['personal_info']['name']
            profession = profile['profession']
            skills_count = len(profile['profileData']['skills'].split(', '))
            
            print(f"✅ {i+1}/{num_profiles}: Added {name} - {profession} ({skills_count} skills)")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error adding profile {i+1}: {str(e)}")
    
    print("\n" + "="*80)
    print(f"✅ SUCCESS: Added {success_count}/{num_profiles} profiles to Firestore")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Check if user specified number of profiles
    num_profiles = 50
    if len(sys.argv) > 1:
        try:
            num_profiles = int(sys.argv[1])
        except ValueError:
            print("Usage: python populate_profiles.py [number_of_profiles]")
            sys.exit(1)
    
    populate_database(num_profiles)
