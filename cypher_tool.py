from typing import Any, List, Tuple, Type, Optional
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field

from llm import llm
import utils as utl

from cypher_generator import GraphCypherQAChainCustom
from langchain.tools import BaseTool



class CypherInput(BaseModel):
    input_str: str = Field(description="extract the entire input question")


class GraphCypherTool(BaseTool):
    name = "CypherTool"
    description = ("this tool uses Input question and invokes _run() function \
                   which returns a cypher query")
    args_schema: Type[BaseModel] = CypherInput

    def _run(
            self,
            input_str: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        cypher_prompt = PromptTemplate(input_variables=["question", "schema"],
                                       template=""" Task:
Generate a Cypher query to retrieve the requested information from a Locates Management System graph database.

Instructions:
Analyze the user question to identify the intent (e.g., retrieving locates, tickets, drivers, or violations).
Determine relevant nodes, relationships, and properties that need to be queried based on the schema.
Apply filters dynamically based on user input (e.g., by Locate ID, region, ticket status, violation type, or date ranges).
For all text-based filtering (e.g., status, type, name, violation type), use CONTAINS instead of = to enable flexible text matching.
Ensure case-insensitive matching by converting text values to lowercase (toLower()) or uppercase (toUpper()) where applicable.
Construct a Cypher query that efficiently retrieves the necessary data.
for overdue or any timeliness check dont check for status also, ensure date fileds are typecasted to date
Output only the Cypher query—do not provide explanations, alternative queries, or extra information.

Nodes and Their Attributes:
Locate:
id: Unique identifier for the locate (Integer).
creationDate: Date the locate request was created (Datetime).
due_date: Deadline for completing the locate (Datetime).
status: Current status of the locate request (String).
type: Type of locate request (String).
region: Geographic region of the locate request (String).
company: Company responsible for the locate (String).
Ticket:
id: Unique identifier for the ticket (Integer).
status: Current status of the ticket (String).
type: Type of service required (String).
priority: Priority level of the ticket (String).
region: Geographic region of the ticket (String).
source: Source of the ticket request (String).
Driver:
id: Unique identifier for the driver (Integer).
name: Full name of the driver (String).
Violation:
violation: Type of violation (String).
Procedure:
id: Unique identifier for the procedure (String).
name: Name of the procedure (String).
instructions: List of step-by-step instructions for the procedure (List of Strings).
Relationships Between Nodes:
(:Locate) -[:HAS_TICKET]-> (:Ticket)
(:Ticket) -[:ASSIGNED_TO]-> (:Driver)
(:Driver) -[:HAS_VIOLATION]-> (:Violation)
Query Generation Logic:
If the user asks about Locates, retrieve relevant locates.
If the user asks about Tickets, retrieve associated tickets with filters.
If the user asks about Drivers, return driver details.
If the user asks about Violations, return only relevant violations.
If the user includes filters (e.g., date ranges, regions, statuses), apply them dynamically.
If the user asks about Procedures, return relevant procedures with instructions.
Input:
User Question: "{question}"
Schema: "{schema}"
Output:
A well-formed Cypher query based on the user question. The query should be dynamically generated with appropriate conditions.


""")
        chain = GraphCypherQAChainCustom.from_llm(graph=utl.graph, cypher_llm=llm, cypher_prompt=cypher_prompt,qa_llm=llm,verbose=True)
        result = chain.run(input_str)
        print("----------------------------------tool op:-----------------------",result)
        return result
