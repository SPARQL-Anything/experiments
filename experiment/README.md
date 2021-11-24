# Evaluation

We conducted a comparative evaluation of sparql.anything with respect to the state of art methods RML and SPARQL Generate.

## Cognitive Complexity Comparison

*Objective*: The objective of the experiment is to compare SPARQL anything with [SPARQL generate](https://ci.mines-stetienne.fr/sparql-generate/), [RML](https://rml.io/) and [ShExML](http://shexml.herminiogarcia.com/)  frameworks in terms of usability and learnability of the frameworks. Specifically,  from the data sources of the SPICE project  we selected four non-RDF resources and for each resource we defined two kinds of tests: one aimed at assessing the usability and learnability of sparql.anything and [SPARQL generate](https://ci.mines-stetienne.fr/sparql-generate/) in retrieving data, the other meant at evaluating  the usability and learnability of four approaches   in generating data. 

*Approach*: As far as retrieval tests is concerned, we inspected the resources in order to identify a set of possible competency questions a user may want to ask. Then, for each competency question we defined the corresponding query according to SPARQL Anything and [SPARQL generate](https://ci.mines-stetienne.fr/sparql-generate/) frameworks.
Concerning the generation tests, for each resource we defined a target RDF model for exporting the data and the rules needed for transforming the data according to each of the compared frameworks.

*Results*: One effective measure of complexity is the number of distinct items or variables that need to be combined within a query or expression [(Halford et al. 2004)](https://www.tandfonline.com/doi/pdf/10.1080/13546780442000033?casa_token=4fEYMB3PswAAAAAA:wfaeKgz51sDOGKdq2KWDn38Iu-Pah0iGmXxMoG6SJIu1Zxv9PR7fcTuFLCdGTnNgiyh8YhamfjeZ). Such a measure of complexity has previously been used to explain difficulties in the comprehensibility of Description Logic statements [(Warren et al. 2015)](https://dl.acm.org/doi/abs/10.1145/2814864.2814866?casa_token=BLtmqOwo4ZUAAAAA:DYqfYy_tnY2GebHD2aG7NBDt2MjT6raKKBNJsrQj1HPofuFnVaykpETzu-PA-YPaShIUT1cUujU). 
Specifically, we counted the number of tokens needed for expressing a set of competency questions.
The queries were tokenized (by using ``"(){},;{}\n\t\r `` as token delimiters) and we computed the total number of tokens  and the number of distinct tokens needed for each queries. 



![Number of Distinct Token per Query](/experiment/img/number_of_tokens.png)![Number of Distinct Token per Query](/experiment/img/number_of_distinct_tokens.png)


*Running the experiment*: The code implementing the tokenizer that has been used for the experiment can be found in the [sparql.anything.experiment module](/sparql.anything.experiment).
The experiment can be run with following command:

```
./run_cog_experiment.sh
```


## Performance Comparison
We assessed the performace of sparql.anything, [SPARQL generate](https://ci.mines-stetienne.fr/sparql-generate/), [RML](https://rml.io/) and [ShExML](http://shexml.herminiogarcia.com/) frameworks in retrieving and generating RDF data.  All of the tests described below were run three times and the average time among the three executions is reported. For practical reasons, for each test we set a 3 minutes timeout.
The tests were executed on a MacBook Pro 2020 (CPU: i7 2.3 GHz, RAM: 32GB).

### Performace in retrieving RDF data
The following Figure shows the time needed for evaluating the SELECT queries q1-q8 and for generating the RDF triples according to the CONSTRUCT queries/mapping rules q9-q12.

![Execution time per  query](/experiment/img/execution_time_queries.png)

ShExML implementation exceeded the timeout for q9-q12.

### Performance in generating RDF data

We also measured the performance in transforming input of increasing size. 
To do so, we  repeatedly concatenated the data sources in order to obtain a JSON array containing 1M JSON objects and we cut this array at length 10, 100, 1K, 10K and 100K.
We ran the query/mapping q12 on these files and we measured the execution time which is shown in the following figure:

![Execution time per  query](/experiment/img/chart_log.png)

ShExML implementation exceeded the timeout for input greater than 1K.

All the perfomance comparisons can be run with the following command:

```
./run_performance_experiment.sh
```


## Queries

In the following the queries used for the experiment are reported.

### Sources: [1](/experiment/data/COLLEZIONI_FONDO_GABINIO_MARZO_2017%20json.json) [2](/experiment/data/COLLEZIONI_GAM.json) [3](/experiment/data/COLLEZIONI_MAO.json)

#### Structure of the input files

```
[
...
 {
   "Autore": "GABINIO MARIO",
   "Titolo": "TORINO/ MONUMENTO A CARLO ALBERTO, PIAZZA CARLO ALBERTO, VISTA LATERALE DESTRA",
   "Datazione": "19/10/1923",
   "Tecnica": "STAMPA ALLA CELLOIDINA",
   "Dimensioni": "229X169",
   "Immagine": "http://93.62.170.226/foto/gabinio/001B1.jpg"
 },
 ...
]

```

#### Competency questions

##### CQ1: What are the titles of the artworks attributed to "ANONIMO"?


[SPARQL Generate query](sparql-generate-queries/q1.rqg) - [SPARQL Anything query](sparql-anything-queries/q1.rqg)


##### CQ2: What are the titles of the artworks made with the technique named "STAMPA ALLA GELATINA CLOROBROMURO D'ARGENTO"?


[SPARQL Generate query](sparql-generate-queries/q2.rqg) - [SPARQL Anything query](sparql-anything-queries/q2.rqg)

##### CQ3: What are the titles of the artworks created in the 1935?


[SPARQL Generate query](sparql-generate-queries/q3.rqg) - [SPARQL Anything query](sparql-anything-queries/q3.rqg)

#### RDF Generation

##### Target model

```
@prefix ex: <http://example.org/> .
_:0 ex:Autore "GABINIO MARIO";
  ex:Datazione "19/10/1923";
  ex:Dimensioni "229X169";
  ex:Immagine "http://93.62.170.226/foto/gabinio/001B1.jpg";
  ex:Tecnica "STAMPA ALLA CELLOIDINA";
  ex:Titolo "TORINO/ MONUMENTO A CARLO ALBERTO, PIAZZA CARLO ALBERTO, VISTA LATERALE DESTRA" .
```
	
[SPARQL Generate query](sparql-generate-queries/q10.rqg) - [SPARQL Anything query](sparql-anything-queries/q10.rqg)  - [RML Mapping](rml-mappings/m2.ttl) - [ShExML Mapping](shexml-mappings/q10.shexml) 

[SPARQL Generate query](sparql-generate-queries/q11.rqg) - [SPARQL Anything query](sparql-anything-queries/q11.rqg) - [RML Mapping](rml-mappings/m3.ttl) - [ShExML Mapping](shexml-mappings/q11.shexml)

[SPARQL Generate query](sparql-generate-queries/q12.rqg) - [SPARQL Anything query](sparql-anything-queries/q12.rqg) - [RML Mapping](rml-mappings/m4.ttl) - [ShExML Mapping](shexml-mappings/q12.shexml)


### Source [4](https://raw.githubusercontent.com/spice-h2020/sparql.anything/main/experiment/data/COLLEZIONI_PALAZZO_MADAMA_marzo2017.json)


#### Structure of the input files


```
[
...
{
	"Inventario": "1110/B",
	"Autore": "Ignoto",
	"Ambito culturale": "",
	"Datazione": "inizio XVI secolo",
	"Titolo-soggetto": "Abramo con tre angeli",
	"Materiali": "bronzo",
	"Immagine": "http://93.62.170.226/foto/1110_B.jpg",
	"lsreferenceby": "http://www.palazzomadamatorino.it/it/node/24055"
}
...
]

```

#### Competency questions

##### CQ4: What are the identifiers of the artworks made of "bronzo"?


[SPARQL Generate query](sparql-generate-queries/q4.rqg) - [SPARQL Anything query](sparql-anything-queries/q4.rqg)


##### CQ5: What are the identifiers of the artworks whose subject is "manifattura Hochst"?

[SPARQL Generate query](sparql-generate-queries/q5.rqg) - [SPARQL Anything query](sparql-anything-queries/q5.rqg)



##### CQ6: How many artworks are made of bronzo?


[SPARQL Generate query](sparql-generate-queries/q6.rqg) - [SPARQL Anything query](sparql-anything-queries/q6.rqg)



##### CQ7: How many artworks each author has made?

[SPARQL Generate query](sparql-generate-queries/q7.rqg) - [SPARQL Anything query](sparql-anything-queries/q7.rqg)



##### CQ8: What is the average number of artworks per author?

[SPARQL Generate query](sparql-generate-queries/q8.rqg) - [SPARQL Anything query](sparql-anything-queries/q8.rqg)



#### RDF Generation

##### Target model

```
@prefix ex: <http://example.org/> .

_:0 ex:Ambito_culturale "";
  ex:Autore "Ignoto";
  ex:Datazione "inizio XVI secolo";
  ex:Immagine "http://93.62.170.226/foto/1110_B.jpg";
  ex:Inventario "1110/B";
  ex:Materiali "bronzo";
  ex:Titolo-soggetto "Abramo con tre angeli";
  ex:lsreferenceby "http://www.palazzomadamatorino.it/it/node/24055" .
```

[SPARQL Generate query](sparql-generate-queries/q9.rqg) - [SPARQL Anything query](sparql-anything-queries/q9.rqg) - [RML Mapping](rml-mappings/m1.ttl) - [ShExML Mapping](shexml-mappings/q9.shexml)



