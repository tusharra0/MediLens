import chromadb

client = chromadb.HttpClient(
  ssl=True,
  host='api.trychroma.com',
  tenant='c62ca6f6-ebde-4f3e-a727-885904e35df1',
  database='MediLens',
  headers={
    'x-chroma-token': 'ck-DhNfVgeXRLgL42wfYfSzqBbBs89Mbzp3gE4SCKrwX3as'
  }
)

# Get your existing collection by name
collection = client.get_collection(name="medical")

example_docs = [
    {
        "id": "1",
        "text": """Overview
Anemia is a problem of not having enough healthy red blood cells or hemoglobin to carry oxygen to the body's tissues. Hemoglobin is a protein found in red cells that carries oxygen from the lungs to all other organs in the body. Having anemia can cause tiredness, weakness and shortness of breath.

There are many forms of anemia. Each has its own cause. Anemia can be short term or long term. It can range from mild to severe. Anemia can be a warning sign of serious illness.

Treatments for anemia might involve taking supplements or having medical procedures. Eating a healthy diet might prevent some forms of anemia.

Products & Services
A Book: Living Medicine
Types
Aplastic anemia
Iron deficiency anemia
Sickle cell anemia
Thalassemia
Vitamin deficiency anemia
Symptoms
Anemia symptoms depend on the cause and how bad the anemia is. Anemia can be so mild that it causes no symptoms at first. But symptoms usually then occur and get worse as the anemia gets worse.

If another disease causes the anemia, the disease can mask the anemia symptoms. Then a test for another condition might find the anemia. Certain types of anemia have symptoms that point to the cause.

Possible symptoms of anemia include:

Tiredness.
Weakness.
Shortness of breath.
Pale or yellowish skin, which might be more obvious on white skin than on Black or brown skin.
Irregular heartbeat.
Dizziness or lightheadedness.
Chest pain.
Cold hands and feet.
Headaches.
When to see a doctor
Make an appointment with your health care provider if you're tired or short of breath and don't know why.

Low levels of the protein in red blood cells that carry oxygen, called hemoglobin, is the main sign of anemia. Some people learn they have low hemoglobin when they donate blood. If you're told that you can't donate because of low hemoglobin, make a medical appointment.

Diagnosis
To diagnose anemia, your health care provider is likely to ask you about your medical and family history, do a physical exam, and order blood tests. Tests might include:

Complete blood count (CBC). A CBC is used to count the number of blood cells in a sample of blood. For anemia, the test measures the amount of the red blood cells in the blood, called hematocrit, and the level of hemoglobin in the blood.

Typical adult hemoglobin values are generally 14 to 18 grams per deciliter for men and 12 to 16 grams per deciliter for women. Typical adult hematocrit values vary among medical practices. But they're generally between 40% and 52% for men and 35% and 47% for women.

A test to show the size and shape of the red blood cells. This looks at the size, shape and color of the red blood cells.
Other diagnostic tests
If you get a diagnosis of anemia, you might need more tests to find the cause. Sometimes, it can be necessary to study a sample of bone marrow to diagnose anemia.

Care at Mayo Clinic
Our caring team of Mayo Clinic experts can help you with your anemia-related health concerns.
Start Here
More Information
Anemia care at Mayo Clinic
Colonoscopy
Complete blood count (CBC)
Treatment
Anemia treatment depends on the cause.

Iron deficiency anemia. Treatment for this form of anemia usually involves taking iron supplements and changing the diet.

If the cause of iron deficiency is loss of blood, finding the source of the bleeding and stopping it is needed. This might involve surgery.

Vitamin deficiency anemias. Treatment for folic acid and vitamin B-12 deficiency involves dietary supplements and increasing these nutrients in the diet.

People who have trouble absorbing vitamin B-12 from food might need vitamin B-12 shots. At first, the shots are every other day. In time, the shots will be shots just once a month, possibly for life.

Anemia of chronic disease. Treatment for this type of anemia focuses on the disease that's causing it. If symptoms become severe, treatment might include getting blood, called a transfusion, or shots of a hormone called erythropoietin.
Anemias associated with bone marrow disease. Treatment of these various diseases can include medicines, chemotherapy or getting bone marrow from a donor, called a transplant.
Aplastic anemia. Treatment for this anemia can include blood transfusions to boost levels of red blood cells. A bone marrow transplant might be needed if bone marrow can't make healthy blood cells.
Hemolytic anemias. Managing hemolytic anemias includes stopping medicines that might be causing it and treating infections. If the immune system is attacking red blood cells, treatment might involve taking medicines that lower immune system activity.
Sickle cell anemia. Treatment might include oxygen, pain relievers, and hydration with fluids given through a vein, called intravenous, to reduce pain and prevent complications. Receiving blood, called a transfusion, and taking folic acid supplements and antibiotics might be involved.

A cancer drug called hydroxyurea (Droxia, Hydrea, Siklos) also is used to treat sickle cell anemia.

Thalassemia. Most forms of thalassemia are mild and need no treatment. More-severe forms of thalassemia generally require blood transfusions, folic acid supplements, medicines, a blood and bone marrow stem cell transplant, or, rarely, removing the spleen.
""",
    },
    {
        "id": "2",
        "text": """
Overview
What is kidney disease? An expert explains
Learn more from kidney doctor Andrew Bentall, M.D.



Show transcript
for video What is kidney disease? An expert explains
Chronic kidney disease, also called chronic kidney failure, involves a gradual loss of kidney function. Your kidneys filter wastes and excess fluids from your blood, which are then removed in your urine. Advanced chronic kidney disease can cause dangerous levels of fluid, electrolytes and wastes to build up in your body.

In the early stages of chronic kidney disease, you might have few signs or symptoms. You might not realize that you have kidney disease until the condition is advanced.

Treatment for chronic kidney disease focuses on slowing the progression of kidney damage, usually by controlling the cause. But, even controlling the cause might not keep kidney damage from progressing. Chronic kidney disease can progress to end-stage kidney failure, which is fatal without artificial filtering (dialysis) or a kidney transplant.

How kidneys work


Show transcript
for video How kidneys work
Products & Services
A Book: Mayo Clinic Family Health Book
Show more products from Mayo Clinic
Symptoms
Signs and symptoms of chronic kidney disease develop over time if kidney damage progresses slowly. Loss of kidney function can cause a buildup of fluid or body waste or electrolyte problems. Depending on how severe it is, loss of kidney function can cause:

Nausea
Vomiting
Loss of appetite
Fatigue and weakness
Sleep problems
Urinating more or less
Decreased mental sharpness
Muscle cramps
Swelling of feet and ankles
Dry, itchy skin
High blood pressure (hypertension) that's difficult to control
Shortness of breath, if fluid builds up in the lungs
Chest pain, if fluid builds up around the lining of the heart
Signs and symptoms of kidney disease are often nonspecific. This means they can also be caused by other illnesses. Because your kidneys are able to make up for lost function, you might not develop signs and symptoms until irreversible damage has occurred.

When to see a doctor
Make an appointment with your doctor if you have signs or symptoms of kidney disease. Early detection might help prevent kidney disease from progressing to kidney failure.

If you have a medical condition that increases your risk of kidney disease, your doctor may monitor your blood pressure and kidney function with urine and blood tests during office visits. Ask your doctor whether these tests are necessary for you.

Diagnosis
Kidney disease FAQs
Nephrologist Andrew Bentall, M.D., answers the most frequently asked questions about kidney disease.



Show transcript
for video Kidney disease FAQs
Kidney biopsy
Kidney biopsy
Enlarge image
As a first step toward diagnosis of kidney disease, your doctor discusses your personal and family history with you. Among other things, your doctor might ask questions about whether you've been diagnosed with high blood pressure, if you've taken a medication that might affect kidney function, if you've noticed changes in your urinary habits and whether you have family members who have kidney disease.

Next, your doctor performs a physical exam, checking for signs of problems with your heart or blood vessels, and conducts a neurological exam.

For kidney disease diagnosis, you might also need certain tests and procedures to determine how severe your kidney disease is (stage). Tests might include:

Blood tests. Kidney function tests look for the level of waste products, such as creatinine and urea, in your blood.
Urine tests. Analyzing a sample of your urine can reveal abnormalities that point to chronic kidney failure and help identify the cause of chronic kidney disease.
Imaging tests. Your doctor might use ultrasound to assess your kidneys' structure and size. Other imaging tests might be used in some cases.
Removing a sample of kidney tissue for testing. Your doctor might recommend a kidney biopsy, which involves removing a sample of kidney tissue. Kidney biopsy is often done with local anesthesia using a long, thin needle that's inserted through your skin and into your kidney. The biopsy sample is sent to a lab for testing to help determine what's causing your kidney problem.
Care at Mayo Clinic
Our caring team of Mayo Clinic experts can help you with your chronic kidney disease-related health concerns.
""",
    }
]

# populate the collection with example documents
for doc in example_docs:
    collection.add(
        ids=[doc["id"]],
        documents=[doc["text"]],
    )

# Query the collection
results = collection.query(
    query_texts=["Tell me about AI"],
    n_results=2
)


print(results)
