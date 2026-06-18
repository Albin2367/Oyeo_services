import re

with open('page-services.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS before </style>
new_css = """
        /* --- BOUTONS --- */
        .btn-blue {
            display: inline-block;
            background-color: var(--primary-blue);
            color: var(--text-light);
            padding: 14px 30px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 500;
            text-decoration: none;
            transition: var(--transition);
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }

        .btn-blue:hover {
            background-color: #1d3557;
            transform: translateY(-2px);
        }

        /* --- HERO BANNER (NOS SERVICES) --- */
        .services-hero {
            background: linear-gradient(rgba(17, 34, 64, 0.65), rgba(17, 34, 64, 0.55)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1920&q=80') no-repeat center center/cover;
            padding: 100px 20px;
            text-align: center;
            color: var(--text-light);
        }

        .services-hero h2 {
            font-size: 3.5rem;
            margin-bottom: 20px;
            font-weight: 400;
        }

        .services-hero p {
            max-width: 650px;
            margin: 0 auto;
            font-size: 0.95rem;
            font-weight: 300;
            opacity: 0.9;
        }

        /* --- BLOCS DE PRESTATIONS --- */
        .prestation-section {
            padding: 80px 0;
        }

        .prestation-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
            margin-bottom: 40px;
        }

        .prestation-row.reverse {
            direction: rtl;
        }

        .prestation-row.reverse .prestation-info,
        .prestation-row.reverse .prestation-details-box {
            direction: ltr; 
        }

        .icon-circle {
            width: 45px;
            height: 45px;
            background-color: #f3efe6;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent-gold);
            font-size: 1.2rem;
            margin-bottom: 20px;
        }

        .prestation-info h3 {
            font-size: 2.5rem;
            color: var(--primary-blue);
            margin-bottom: 15px;
        }

        .prestation-description {
            font-size: 0.95rem;
            color: #666;
            font-style: italic;
            max-width: 450px;
        }

        .prestation-details-box {
            background-color: var(--card-bg);
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
            border: 1px solid rgba(0, 0, 0, 0.03);
        }

        .features-list {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px 30px;
            list-style: none;
        }

        .features-list li {
            font-size: 0.85rem;
            color: #555;
            position: relative;
            padding-left: 18px;
        }

        .features-list li::before {
            content: "•";
            color: var(--accent-gold);
            font-size: 1.2rem;
            position: absolute;
            left: 0;
            top: -2px;
        }

        @media (max-width: 900px) {
            .prestation-row, .prestation-row.reverse {
                grid-template-columns: 1fr;
                gap: 40px;
                direction: ltr;
            }
            .prestation-row.reverse .prestation-info,
            .prestation-row.reverse .prestation-details-box {
                direction: ltr;
            }
            .services-hero h2 {
                font-size: 2.8rem;
            }
            .prestation-info h3 {
                font-size: 2rem;
            }
        }

        @media (max-width: 600px) {
            .features-list {
                grid-template-columns: 1fr;
            }
            .prestation-details-box {
                padding: 25px;
            }
        }
    </style>
"""
content = content.replace('    </style>', new_css)

# 2. Add --bullet-color to :root
content = content.replace('--card-bg: #ffffff;', '--card-bg: #ffffff;\n            --bullet-color: #d8c3a5;')

# 3. Replace the body content
new_html = """    <section class="services-hero">
        <span class="hero-tag">Nos Prestations</span>
        <h2>Nos Services</h2>
        <p>Découvrez notre gamme complète de services privés du quotidien, conçus pour vous faire gagner du temps et vous garantir sérénité et qualité.</p>
    </section>

    <div class="container">

        <div class="prestation-section">
            <div class="prestation-row">
                <div class="prestation-info">
                    <div class="icon-circle"><i class="fa-solid fa-house"></i></div>
                    <h3>Maison Impeccable</h3>
                    <p class="prestation-description">Nous prenons soin de votre intérieur avec discrétion, méthode et exigence.</p>
                    <a href="#" class="btn-blue">Demander cette prestation</a>
                </div>
                <div class="prestation-details-box">
                    <ul class="features-list">
                        <li>Nettoyage premium</li>
                        <li>Repassage</li>
                        <li>Changement des draps</li>
                        <li>Remise en ordre après événement</li>
                        <li>Rangement</li>
                        <li>Pliage du linge</li>
                        <li>Préparation avant réception</li>
                        <li>Entretien avant retour de voyage</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="prestation-section">
            <div class="prestation-row reverse">
                <div class="prestation-info">
                    <div class="icon-circle"><i class="fa-solid fa-mug-hot"></i></div>
                    <h3>Matin Privilège</h3>
                    <p class="prestation-description">Offrez un réveil élégant, préparé et livré avec soin.</p>
                    <a href="#" class="btn-blue">Demander cette prestation</a>
                </div>
                <div class="prestation-details-box">
                    <ul class="features-list">
                        <li>Livraison de petit-déjeuner</li>
                        <li>Fleurs</li>
                        <li>Surprise romantique</li>
                        <li>Brunch familial</li>
                        <li>Viennoiseries</li>
                        <li>Carte personnalisée</li>
                        <li>Anniversaire</li>
                        <li>Attention spéciale au réveil</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="prestation-section">
            <div class="prestation-row">
                <div class="prestation-info">
                    <div class="icon-circle"><i class="fa-solid fa-basket-shopping"></i></div>
                    <h3>Courses & Quotidien</h3>
                    <p class="prestation-description">Nous gérons vos petites urgences et vos courses du quotidien.</p>
                    <a href="#" class="btn-blue">Demander cette prestation</a>
                </div>
                <div class="prestation-details-box">
                    <ul class="features-list">
                        <li>Courses alimentaires</li>
                        <li>Pressing</li>
                        <li>Achat de fleurs</li>
                        <li>Rangement des courses</li>
                        <li>Pharmacie</li>
                        <li>Dépôt et retrait de colis</li>
                        <li>Achat de gâteau</li>
                        <li>Préparation de la maison avant retour</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="prestation-section">
            <div class="prestation-row reverse">
                <div class="prestation-info">
                    <div class="icon-circle"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
                    <h3>Maison Prête</h3>
                    <p class="prestation-description">Préparation avant réception ou retour de voyage.</p>
                    <a href="#" class="btn-blue">Demander cette prestation</a>
                </div>
                <div class="prestation-details-box">
                    <ul class="features-list">
                        <li>Logement aéré</li>
                        <li>Frigo rempli</li>
                        <li>Fleurs disposées</li>
                        <li>Ambiance accueillante</li>
                        <li>Courses faites</li>
                        <li>Linge prêt</li>
                        <li>Maison rangée</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="prestation-section" style="padding-bottom: 120px;">
            <div class="prestation-row">
                <div class="prestation-info">
                    <div class="icon-circle"><i class="fa-solid fa-wine-glass"></i></div>
                    <h3>Après Réception</h3>
                    <p class="prestation-description">Remise en ordre après dîner, fête ou événement privé.</p>
                    <a href="#" class="btn-blue">Demander cette prestation</a>
                </div>
                <div class="prestation-details-box">
                    <ul class="features-list">
                        <li>Vaisselle</li>
                        <li>Nettoyage cuisine</li>
                        <li>Sanitaires</li>
                        <li>Poubelles</li>
                        <li>Sols</li>
                        <li>Rangement général</li>
                    </ul>
                </div>
            </div>
        </div>

    </div>
"""
# We need to replace from `<div class="hero-content"` up to `</section>` (end of services-section)
pattern = re.compile(r'<div class="hero-content".*?</section>', re.DOTALL)
content = pattern.sub(new_html, content)

# 4. Add JS animation logic
new_js = """
            // Effet d'apparition au défilement pour les prestations
            const observerRows = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = "1";
                        entry.target.style.transform = "translateY(0)";
                    }
                });
            }, { root: null, threshold: 0.15 });

            const rows = document.querySelectorAll('.prestation-row');
            rows.forEach(row => {
                row.style.opacity = "0";
                row.style.transform = "translateY(30px)";
                row.style.transition = "all 0.6s ease-out";
                observerRows.observe(row);
            });
"""
# Insert right after `document.addEventListener("DOMContentLoaded", () => {`
content = content.replace('document.addEventListener("DOMContentLoaded", () => {', 'document.addEventListener("DOMContentLoaded", () => {' + new_js)

with open('page-services.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
