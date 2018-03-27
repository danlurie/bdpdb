# Brain Damage Patient Data Browser (BDPDB)
BDPDB is a browser-based application for managing, browsing, and searching demographic information and neuroimaging data from patients with brain injury. For an overview of BDPDB functionality, please see the [poster from OHBM 2017](https://figshare.com/articles/OHBM_2017_Poster_A_Browser-Based_Tool_for_Managing_Searching_and_Viewing_MRI_Data_from_Patients_with_Brain_Lesions/5145298).

## Privacy Warning
BDPDB is designed for use in research settings, and the access controls built in to BDPDB should be considered only as additional safeguards to complement existing institutionally approved security infrastructure and data access protocols for protecting potentially sensitive patient information. There are a few specific points we would like users to be aware of:
- While it is possible to store full DOB information (i.e. year, month, and day) in BDPDB, this data is [often considered personally identifiable and may be subject to specific legal standards for data storage and access](https://privacyruleandresearch.nih.gov/pr_08.asp). BDPDB will work just fine if you set all patients in the database to have a birthday of January 1st.
- Because BDPDB is accessed through a web browser, it will be visible to any user who can connect to the IP address on which the server broadcasts (`localhost` by default). As such, we recommend only running BDPDB on systems where all logged-in users are authorized to access patient data. 

## BDPDB is a work in progress, and should be considered alpha software.
Functionality may change, dissapear, or temporarily cease to function at any time. **Do not rely on BDPDB as the sole location to store your data, or as your main strategy for limiting access to sensitive information**.

