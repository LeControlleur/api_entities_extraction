# Log book

## Topic Decryption

With the help of the clue that was given: "P as in Perfect", I thought of a Cesar cipher which consists in shifting the letters of a certain rank to the right in order to have an encrypted string from a plaintext string. 

So I started by determining the encryption key that corresponds to the shift step. There was a decoding from **A to P**. I had to decode the key in reverse to get the right string.

I also identified another key which corresponded to the letter **k**.
## Global overview

This file aims to explain the differents steps for the creation of the entities extraction.

The fisrt step is to determine the differents elements that will constitue our tool. Thus, the tool consists of 2 main services that are the extraction of entities and the statistics service. These two main services are in the **utils** folder.

The test files for these files are located in the **test** folder.

The approach that was used is TDD (Test Driven Development). So for each service, a test is written. Then the functionality to pass the test is written. Thus, in an iterative way, each service has been developed whether it is for the extraction of entities or the statistics.

## Text analysis

The first step of the text analysis is the extraction of entities. The text to be analyzed is passed as a parameter for the extraction of entities by TextRazor. The result of this extraction contains all the entities present in our text (animals, countries, persons, ...). We filter these entities in order to keep only the persons. 

The elements obtained with this entity extraction are however not exhaustive. It is therefore necessary to enrich the results with additional information such as occupation, date and place of birth and other information. So we use a Wikidata client to enrich the different entities.

The result is return by the function.

At the same, on another thread, the elements that make up the result are stored in a database for later use. Another thread is used so that the data recording time, which is not part of the processing, has an impact on the waiting time of the client.

## Statistics computation

The first function of statistics processing is in charge of recording the information necessary for the determination of the stats. When the API is launched, a database and the necessary tables are created if they do not already exist.

The database has been designed so that the number of records is not infinite. Therefore, instead of recording each unique occurrence, the value is recorded the first time and the number of occurrences is incremented at each new record will for the same value.

La détermination des occurence les plus fréquentes se fait par simple requête SQL.

## API

Once the different functionalities are developed, the API is set up with the definition of the tests for the routes and the results that each call should return. These tests led to the development of the API routes.

We have a POST route for text parsing and a GET route for retrieving statistics. This small number of routes with simple parameters was set to put the complexity on the developer's side and not the client's.

## Ideas for improvement

The enrichment of the entities takes quite a long time. This delay is mainly caused by the fact that each key belonging to the received data is compared to the keys we need for enrichment. It would therefore be ideal to find a direct indexing method, which would reduce the complexity of verification from linear to constant.