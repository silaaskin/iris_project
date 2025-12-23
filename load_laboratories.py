# manage.py shell'de çalıştırın:
# python manage.py shell
# exec(open('load_laboratories.py').read())

from iris_app.models import Laboratory

# Mevcut laboratuvarları kontrol et
existing = Laboratory.objects.count()

if existing == 0:
    laboratories_data = [
        {
            'name': 'Istanbul Botanical Research Center',
            'city': 'Istanbul',
            'country': 'Turkey',
            'phone': '+90-212-555-0001',
            'email': 'contact@istanbul-botanics.org',
            'established_year': 1995,
            'description': 'Leading botanical research center in Turkey specializing in Iris classification and breeding.'
        },
        {
            'name': 'Ankara National Herbarium',
            'city': 'Ankara',
            'country': 'Turkey',
            'phone': '+90-312-555-0002',
            'email': 'info@ankara-herbarium.gov.tr',
            'established_year': 1985,
            'description': 'National herbarium with extensive Iris specimen collection and preservation.'
        },
        {
            'name': 'Izmir University Plant Science Lab',
            'city': 'Izmir',
            'country': 'Turkey',
            'phone': '+90-232-555-0003',
            'email': 'lab@izmir-university.edu.tr',
            'established_year': 2001,
            'description': 'Academic laboratory focused on plant genetics and phenotypic analysis.'
        },
        {
            'name': 'Mediterranean Botanical Institute',
            'city': 'Antalya',
            'country': 'Turkey',
            'phone': '+90-242-555-0004',
            'email': 'research@med-botanics.org',
            'established_year': 1998,
            'description': 'Research institute studying Mediterranean flora including various Iris species.'
        },
        {
            'name': 'Royal Botanic Gardens',
            'city': 'London',
            'country': 'United Kingdom',
            'phone': '+44-20-8332-5000',
            'email': 'info@kew.org',
            'established_year': 1840,
            'description': 'Prestigious international botanical gardens with world-class Iris collection.'
        },
        {
            'name': 'Berlin Botanical Museum',
            'city': 'Berlin',
            'country': 'Germany',
            'phone': '+49-30-838-50100',
            'email': 'contact@botanischergarten.berlin',
            'established_year': 1899,
            'description': 'Museum and botanical research center with diverse plant species collection.'
        },
    ]

    # Laboratuvarları oluştur
    for lab_data in laboratories_data:
        lab = Laboratory.objects.create(**lab_data)
        print(f"✅ {lab.name} created")
    
    print(f"\n✅ Toplam {len(laboratories_data)} laboratories added successfully!")
else:
    print(f"⚠️ Zaten {existing} laboratories already exist in the database.")