# Rats, Rodents, and New York City

## Final Writeup

**Eric Trautsch**

**BAIS:6140 Information Visualization**

**Fall 2023**

![Project Logo](assets/ratlogo.png)

### Executive Summary

Teaser image (around cental theme)

Description of storyline

Bid idea or three minute story or summmary of each slide and interactive dashboard

### Data

When developing the interactive graph that allows for the selection of a particular community board, I discovered inconsistencies in the data relating to the Borough and Community Board relationship. I fixed this by ensuring that any community board MUST contain the name of the Borough to display, ensuring that these data collection errors are not shown.

![Data Cleaning For Borough Relationships](assets/DataCleaningIssue.png)

### Visualizations

When creating the line chart, I noticed that many Boroughs tended to improve their data collection and no longer attribute sightings to Unspecified community boards. To not allow this change in process to affect the visualization too much, I limited the line charts on that to not go beyond 2018. Otherwise, the increase across the board may be attributed to something other than data collection practices.

### Usage Scenario

A typical user, possibly an NYC resident, discovers the application through a QR code scanned in the subway. They are directed to the web address, where they can interact with the story.

![Rat Sightings Over Time Animation](assets/AnimationOfHistoricalSightingsOverTime.png)

The platform is optimized for both web and mobile, enabling quick interaction with detailed visualizations and calls to action.

![Call to Action](assets/CalltoAction.png)

### Reflection


### Project Management and Team Assessment

| **Task**                | **Completed** | **Estimated Hours** | **Actual Hours** |
| ----------------------- | ------------- | ------------------- | ---------------- |
| Project Proposal        | 11/02/2023    | 6                   | 5                |
| EDA                     | 11/09/2023    | 1                   | 3                |
| Iteration 1 complete    | 11/12/2023    | 8                   | 5                |
| Iteration 2 complete    | 11/28/2023    | 7                   | 7.5              |
| Final Presentation      |               | 5                   |                  |
| Final Recording         |               | 2                   |                  |
| Final writeup completed |               | 10                  |                  |

All work was completed by Eric (only member of the project team).

### Credits

- NYC OpenData
- Course Notes
- The Dash and Plotly projects
  - Built heavily upon the dash framework to host and manage application
- Microsoft Azure for deployment