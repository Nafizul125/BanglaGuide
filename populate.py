from django.conf import settings
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banglaguide.settings')
django.setup()

from tourism.models import Division, District, TouristSpot

# Divisions and their districts
divisions = {
    'Dhaka': ['Dhaka', 'Tangail'],
    'Chittagong': ['Chittagong', "Cox's Bazar", 'Bandarban'],
    'Khulna': ['Khulna', 'Bagerhat'],
    'Rajshahi': ['Rajshahi', 'Bogura'],
    'Rangpur': ['Rangpur', 'Dinajpur'],
    'Mymenshingh': ['Mymenshingh'],
    'Sylhet': ['Sylhet'],
    'Barishal': ['Barishal', 'Patuakhali'],
}

# Create divisions and districts
for div_name, districts in divisions.items():
    div, _ = Division.objects.get_or_create(name=div_name)
    for dist_name in districts:
        District.objects.get_or_create(name=dist_name, division=div)

# Tourist Spots
# Dhaka Division
dhaka_dist = District.objects.get(name='Dhaka')
TouristSpot.objects.get_or_create(
    name='Ahsan Manzil',
    district=dhaka_dist,
    defaults={'description': 'Ahsan Manzil is a historical palace located in the Kumartoli area beside Buriganga River of Dhaka, Bangladesh. It was formerly the residence and seat of the Nawab of Dhaka and has been designated an Old Dhaka Heritage Site. It now serves as a museum. The ticket price is 40 taka.'}
)
TouristSpot.objects.get_or_create(
    name='Lalbagh Fort',
    district=dhaka_dist,
    defaults={'description': 'The Lalbagh Fort is a historic fort situated in the old city of Dhaka, Bangladesh. Its name is derived from its neighbourhood Lalbagh, which means Red Garden. The term Lalbagh refers to reddish and pinkish hues in the Mughal architecture. The original fort was called Fort Aurangabad. Its construction was started by Prince Muhammad Azam Shah, who was the son of Emperor Aurangzeb and briefly a future Mughal emperor himself.'}
)

tangail_dist = District.objects.get(name='Tangail')
TouristSpot.objects.get_or_create(
    name='Mohera Jamider Bari',
    district=tangail_dist,
    defaults={'description': 'Mohera Zamindar Bari is a 19th-century Zamidari residence in Mirzapur, Tangail District, Bangladesh'}
)

# Chittagong Division
chittagong_dist = District.objects.get(name='Chittagong')
TouristSpot.objects.get_or_create(
    name='Bhatiary',
    district=chittagong_dist,
    defaults={'description': 'Bhatiary union is located in the southern part of Sitakunda upazila, just 15 kilometers away from Chittagong city. Bhatiary is full of natural beauty with green mountains, crystal clear lake water, army-controlled golf courses.'}
)
TouristSpot.objects.get_or_create(
    name='Patenga Sea Beach',
    district=chittagong_dist,
    defaults={'description': "Patenga Sea Beach is a popular destination located 14 kilometers south of Chittagong city, Bangladesh, near the mouth of the Karnaphuli River. It's known for its vibrant atmosphere, street food, and opportunities for water sports."}
)

cox_dist = District.objects.get(name="Cox's Bazar")
TouristSpot.objects.get_or_create(
    name='Inani Beach',
    district=cox_dist,
    defaults={'description': "Inani Beach, part of Cox's Bazar Beach, is a popular 18-kilometer long sea beach in Ukhia Upazila, Cox's Bazar, Bangladesh. It is known for its unique coral stones, which appear green during the summer and rainy seasons."}
)
TouristSpot.objects.get_or_create(
    name='Himchari Fountain',
    district=cox_dist,
    defaults={'description': 'Shallow waterfall located in a national park, popular for sunset views over the sea.'}
)

bandarban_dist = District.objects.get(name='Bandarban')
TouristSpot.objects.get_or_create(
    name='Nilachal',
    district=bandarban_dist,
    defaults={'description': 'Nilachal is the nearest tourist spot from Bandarban. It is situated at Tigerpara and about 2000 feet above the sea level and 5 kilometers away from the Bandarban town.'}
)
TouristSpot.objects.get_or_create(
    name='Thanchi',
    district=bandarban_dist,
    defaults={'description': 'Thanchi is an upazila of Bandarban District in the Division of Chittagong, Bangladesh.'}
)

# Khulna Division
khulna_dist = District.objects.get(name='Khulna')
TouristSpot.objects.get_or_create(
    name='Sundarbans',
    district=khulna_dist,
    defaults={'description': "The Sundarbans, the world's largest mangrove forest, is located in the delta region where the Ganges, Brahmaputra, and Meghna rivers meet the Bay of Bengal."}
)

bagerhat_dist = District.objects.get(name='Bagerhat')
TouristSpot.objects.get_or_create(
    name='Shat Gombuj Mosque',
    district=bagerhat_dist,
    defaults={'description': 'The Sixty Dome Mosque is a historical mosque, located in Bagerhat, in the Khulna Division of Bangladesh. It is a part of the Mosque City of Bagerhat, a UNESCO World Heritage Site.'}
)

# Rajshahi Division
rajshahi_dist = District.objects.get(name='Rajshahi')
TouristSpot.objects.get_or_create(
    name='T- Badh',
    district=rajshahi_dist,
    defaults={'description': 'T-Badh is one of the most popular places to visit in the Rajshahi City.'}
)
TouristSpot.objects.get_or_create(
    name='University of Rajshahi',
    district=rajshahi_dist,
    defaults={'description': 'The University of Rajshahi, also known as Rajshahi University, is a public research university located in Rajshahi, Bangladesh.'}
)

bogura_dist = District.objects.get(name='Bogura')
TouristSpot.objects.get_or_create(
    name='Mahasthangarh',
    district=bogura_dist,
    defaults={'description': 'Mahasthangarh is the oldest archaeological site in Bangladesh. It dates back to 300 BCE and was the ancient capital of the Pundra Kingdom.'}
)
TouristSpot.objects.get_or_create(
    name='Kalitola Ghat',
    district=bogura_dist,
    defaults={'description': 'Kali Thola Ghat is a station in Sariakandi, Bogra District'}
)

# Rangpur Division
dinajpur_dist = District.objects.get(name='Dinajpur')
TouristSpot.objects.get_or_create(
    name='Kantajew Temple',
    district=dinajpur_dist,
    defaults={'description': 'Kantojiu Temple at Kantanagar is a late-medieval Hindu temple in Dinajpur District, Bangladesh. It was built by Maharaja Pran Nath; its construction started in 1702 and ended in 1752, during the reign of his son Maharaja Ramnath.'}
)
TouristSpot.objects.get_or_create(
    name='Ramsagar',
    district=dinajpur_dist,
    defaults={'description': 'Ramsagar is a small lake located in the village Tajpur in Dinajpur District, Bangladesh.'}
)

rangpur_dist = District.objects.get(name='Rangpur')
TouristSpot.objects.get_or_create(
    name='Tajhat Palace',
    district=rangpur_dist,
    defaults={'description': 'Tajhat Palace or Tajhat Rajbari is a historic palace in Rangpur, Bangladesh. This palace now holds the Rangpur museum.'}
)
TouristSpot.objects.get_or_create(
    name='Begum Rokeya Memorial',
    district=rangpur_dist,
    defaults={'description': 'Begum Rokeya House.'}
)

# Mymenshingh Division
mymenshingh_dist = District.objects.get(name='Mymenshingh')
TouristSpot.objects.get_or_create(
    name='Muktagacha Jomidar Bari',
    district=mymenshingh_dist,
    defaults={'description': 'Muktagacha Zamindar Bari or Aat Ani Zamindar Bari is an ancient zamindar palace located in Muktagacha Upazila of Mymensingh District, Bangladesh.'}
)
TouristSpot.objects.get_or_create(
    name='Shashi Lodge',
    district=mymenshingh_dist,
    defaults={'description': 'The Shashi Lodge, also known as the Rajbari of Mymensingh, was the palace-residence of Maharaja Shashikant Acharya, who was the Maharaja of the Muktagacha Zamindari Estate in Mymensingh of East Bengal during the time of the British Raj in India.'}
)

# Sylhet Division
sylhet_dist = District.objects.get(name='Sylhet')
TouristSpot.objects.get_or_create(
    name='Jaflong',
    district=sylhet_dist,
    defaults={'description': 'Jaflong is a hill station and tourist destination in the Division of Sylhet, Bangladesh.'}
)
TouristSpot.objects.get_or_create(
    name='Sada pathor',
    district=sylhet_dist,
    defaults={'description': 'Bholagonj, Sylhet'}
)

# Barishal Division
barishal_dist = District.objects.get(name='Barishal')
TouristSpot.objects.get_or_create(
    name='Guthia Mosque',
    district=barishal_dist,
    defaults={'description': 'The Baitul Aman Jame Masjid Complex, commonly known as Guthia Mosque of Barisal, is a mosque complex of Barishal'}
)

patuakhali_dist = District.objects.get(name='Patuakhali')
TouristSpot.objects.get_or_create(
    name='Kuakata',
    district=patuakhali_dist,
    defaults={'description': 'Kuakata is a town of Patuakhali located in southern Bangladesh known for its panoramic sea beach.'}
)