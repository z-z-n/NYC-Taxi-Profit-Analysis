# NYC-Taxi-Profit-Analysis
### Introduction
The analysis of potential profit for NYC taxi services involves utilizing a variety of AWS services to assess the potential benefits of picking up passengers in different areas of New York City. Utilizing AWS infrastructure, analysts store the NYC Taxi and Limousine Commission (TLC) dataset as CSV files in S3 buckets. With this extensive dataset, AWS EMR employs Spark to accelerate analysis, processing millions of records stored in S3. This efficient utilization of AWS services facilitates rapid computation and provides valuable insights into the potential benefits of serving passengers in various NYC locations.

### Data Analysis
The TLC (Taxi and Limousine Commission) Trip Record Dataset is a comprehensive collection of taxi trip data maintained by the City of New York. This dataset provides valuable insights into the operation of taxi services within the city, including details such as pickup and drop-off locations, trip duration, fare information, and other relevant metrics. For the project, a subset of the TLC dataset was selected, specifically focusing on Yellow taxis for the month of January 2019. This subset comprises over 7,600,000 individual trip records, offering a rich source of data for analysis and exploration.

At the NYC TLC, this data analysis project aims to pinpoint high-potential pickup spots for taxi drivers, focusing on profitability. By initially identifying the top 100 drop-off locations in New York with PySpark, it becomes evident that Manhattan has a significantly higher volume of drop-offs compared to other boroughs. Following this, the project obtains the 30 most popular drop-off locations in Manhattan, and analyzes all pickup locations citywide, calculating key metrics such as average trip revenue and trip counts. By weighting profits based on the probability of passengers heading to popular destinations, the analysis guides strategic taxi deployment, optimizing service for maximum profitability and meeting passenger demand effectively.

### Visualization
For visualizing the data generated during the analysis, this project primarily establishes a Flask server on an EC2 instance to facilitate interaction with the frontend. The frontend interface reads the CSV analysis results stored in an S3 bucket and utilizes d3.js for visualization. Initially, the project creates a bar chart for the top 100 drop-off locations, color-coded by borough, to provide a visual representation. Subsequently, it calculates the drop-off frequency for each borough. Furthermore, for the weighting profits obtained from the analysis of pickup locations, d3.js is utilized to map these values onto a geographical map, using varying shades of color to indicate the magnitude, with tooltips providing detailed information for each area.

![image](https://github.com/z-z-n/NYC-Taxi-Profit-Analysis/blob/master/Readme/1.jpg)
<p align="center"><strong>Bar chart for the top 100 drop-off locations</strong></p>

![image](https://github.com/z-z-n/NYC-Taxi-Profit-Analysis/blob/master/Readme/4.jpg)
<p align="center"><strong>Bubble chart of the number of drop-offs borough</strong></p>

![image](https://github.com/z-z-n/NYC-Taxi-Profit-Analysis/blob/master/Readme/2.jpg)
<p align="center"><strong>Colored Map of drop-off frequencies</strong></p>

![image](https://github.com/z-z-n/NYC-Taxi-Profit-Analysis/blob/master/Readme/3.jpg)
<p align="center"><strong>Uncolored Map</strong></p>
