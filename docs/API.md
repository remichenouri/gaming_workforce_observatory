# Gaming Workforce Observatory - API Documentation

## Overview
The Gaming Workforce Observatory provides a comprehensive API for accessing gaming industry workforce analytics data and insights.

## Base URL
Production: https://gaming-workforce-observatory.streamlit.app/api/v1
Development:http://localhost:8501/api/v1

text

## Authentication
API Key authentication
curl -H "X-API-Key: your-api-key"
https://gaming-workforce-observatory.streamlit.app/api/v1/employees

text

## Core Endpoints

### Employee Data

#### GET /employees
Get all employee data with optional filtering.

**Parameters:**
- `department` (string): Filter by department (Game Design, Programming, Art, QA, Marketing, Management)
- `level` (string): Filter by level (Junior, Mid, Senior, Lead, Principal)
- `limit` (integer): Limit results (default: 100, max: 1000)
- `offset` (integer): Pagination offset

**Example:**
curl "https://gaming-workforce-observatory.streamlit.app/api/v1/employees?department=Programming&level=Senior"

text

**Response:**
{
"status": "success
, "data
:
[ { "em
loyee_id": 1, "nam
": "Alice Johnson", "d
partment": "Progra
ming", "le
el": "Senior", "sala
y": 95000, "satisfa
tion_score": 8.2,
"performance_score
: 4.5, "gamin
_metrics": { "
p
i
t_
elocity":
42,
"bug_fix_rate
: 88,

text

#### GET /employees/{employee_id}
Get specific employee details.

**Response:**
{
"status": "success
, "data
: { "employee
id": 1, "name": "Ali
e Johnson", "department"
"Programming", "
etailed_metrics": { "quarterly_perf
rmance": [4.2, 4.5, 4.7], "satis
action_trend": [7.8,
8.0, 8.2], "b
r
o
text

### Gaming KPIs

#### GET /kpis
Get all calculated KPIs for the gaming workforce.

**Parameters:**
- `category` (string): KPI category (development, quality, satisfaction, retention)
- `department` (string): Department filter
- `time_period` (string): Time period (7d, 30d, 90d, 1y)

**Example:**
curl "https://gaming-workforce-observatory.streamlit.app/api/v1/kpis?category=development&time_period=30d"

text

**Response:**
{
"status": "success
, "data
: { "sprint_velo
ity": {
value": 42.5,
"target":
0.0, "trend": "up",
"department_br
akdown": { "
rogramming
:
45
2, "Game
esign": 38.7,
"QA": 44
1 } },
"bug_fix_rate": { "value": 87.3,


text

#### GET /kpis/gaming-specific
Get gaming industry specific KPIs.

**Response:**
{
"status": "success
, "data
: { "crunch_impact_s
ore": {
"value": 2.8,
"target": 3.
, "status": "good",

departments_at_risk":
["QA"] },
"innovation_index":
{ "value": 78.5,
"gaming_bench
a
ks
: { "indie_studios
: 82.0,
"aaa_studios": 75.0 }
, "game_launch_r
a
i
text

### Predictions & ML

#### GET /predictions/turnover
Get ML-powered turnover predictions.

**Parameters:**
- `risk_threshold` (float): Risk threshold (0.0-1.0, default: 0.7)
- `department` (string): Department filter

**Response:**
{
"status": "success
, "data
: { "high_risk_emplo
e
s": [ {
"employee_id": 4
, "name": "
ohn Doe", "d
partment": "QA",
"flight_risk
: 0.82, "ris
_factors": [
"
ow_satisfaction",
"high_crunch_hours",
"no_recent_prom
tion" ], "re
o
m
nd
tions": [ "Sc
edule 1:1 with manager", "Re
u
text

#### POST /predictions/burnout
Predict burnout risk for specific employee.

**Request Body:**
{
"employee_id": 12
, "current_metrics
: { "crunch_hours_last_mon
h": 65, "satisfaction_
core": 6.2, "sprint_veloci
y
text

**Response:**
{
"status": "success
, "data
: { "burnout_risk
: 0.73, "risk_lev
l": "high", "contribu
i
g_factors": [ { "
actor": "exces
iv
_
vertime", "impact": 0.35
}, {


"factor": "declini
g_satisfaction", "impac
": 0.28 } ], "recomm
ndations": [ "Immediate work
o
d
text

### Team Analytics

#### GET /teams
Get team-level analytics.

**Response:**
{
"status": "success
, "data
:
[ { "team_id": "pro
-team-alpha", "name": "Prog
amming Team Alpha", "d
partment":
"Programming
, "size": 8, "me
rics": { "avg_spr
nt_velocity": 45.2,
"team_satisfaction": 8.1,

"collaboration_s
ore": 8.5,
"in
ovation_con
r
b
t
text

### Gaming Industry Benchmarks

#### GET /benchmarks
Get gaming industry benchmarks for comparison.

**Response:**
{
"status": "success
, "data
: { "salary_ra
ges": { "P
ogramming": { "Junior": {"min": 45000, "max": 65
00, "median": 55000}, "Senior": {"min": 80000, "
a
":
120000, "median":
5000} } }, "indus
ry_kpis": { "average_reten
ion_rate": 0.68, "typical_sp
in
_velocity": 38.5, "sta
dard_satisfaction_score": 7.
}, "gaming_specific_metrics
:
{
text

## Data Models

### Employee Model
{
"employee_id": "integer
, "name": "stri
g", "department": "enum[Game Design, Programming, Art, QA, Marketing, Managem
nt]", "level": "enum[Junior, Mid, Senior, Lead, Prin
ipal]", "salary":
"number", "satisfaction_score": "num
er (1-10)", "performance_score": "
umber (1-5)", "years_experie
ce": "integer", "h
re_date": "date",
"gaming_metrics": { "spr
nt_velocity": "number", "bug_
ix_rate": "number (0-100)", "inno
ation_index": "number (0-100)",
crunch_hours_last_month": "number", "te
m
text

### KPI Model
{
"name": "string
, "value": "numb
r", "target": "nu
ber", "trend": "enum[up, down, s
able]", "status": "enum[critical, warning, good, ex
ellent]", "gaming_context
: "string", "last_update
text

## Error Handling

### Error Response Format
{
"status": "error
, "error
: { "code": "INVALID_DEPA
TMENT", "message": "Department 'InvalidDept' is not valid. Valid options: Game Design, Programming, Art, QA, Marketing,
anagement",
"details": { "valid_departments": ["Game Design", "Programming", "Art", "QA", "Mar
e
i
text

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (invalid API key)
- `404` - Resource not found
- `429` - Rate limit exceeded
- `500` - Internal server error

## Rate Limiting
- **Free tier**: 100 requests/hour
- **Premium tier**: 1000 requests/hour
- **Enterprise tier**: Unlimited

## SDKs and Libraries

### Python SDK
from gaming_workforce_sdk import GamingWorkforceClient

client = GamingWorkforceClient(api_key="your-api-key")

Get employees
employees = client.employees.list(department="Programming")

Get KPIs
kpis = client.kpis.get_gaming_specific()

Predict turnover
predictions = client.ml.predict_turnover(risk_threshold=0.7)

text

### JavaScript SDK
import { GamingWorkforceAPI } from 'gaming-workforce-sdk';

const api = new GamingWorkforceAPI('your-api-key');

// Get team analytics
const teams = await api

// Get benchmarks
const benchmarks = await api.benchmarks.

text

## Webhooks

### Setting up Webhooks
curl -X POST "https://gaming-workforce-observatory.streamlit.app/api/v1/webhooks"
-H "X-API-Key: your-api-key"
-H "Content-Type: application/json"
-d '{
https://your-app.com/webhook",
"events": ["employee.high_flight_risk", "team.performance_dro
"], "gaming_triggers": ["crunch_period_detected", "mileston
text

### Webhook Events
- `employee.high_flight_risk` - Employee flight risk > 0.7
- `employee.burnout_risk` - Burnout risk detected
- `team.performance_drop` - Team metrics below threshold
- `gaming.crunch_detected` - Crunch period identified
- `gaming.milestone_risk` - Project milestone at risk

## Support

- **Documentation**: [https://docs.gaming-workforce-observatory.com](https://docs.gaming-workforce-observatory.com)
- **API Status**: [https://status.gaming-workforce-observatory.com](https://status.gaming-workforce-observatory.com)
- **Support Email**: api-support@gaming-workforce-observatory.com
- **Gaming Industry Forum**: [https://community.gaming-workforce-observatory.com](https://community.gaming-workforce-observatory.com)