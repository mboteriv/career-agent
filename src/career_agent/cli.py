from unittest import result

import typer
from career_agent.models.recommendation_options import RecommendationOptions
from career_agent.providers.greenhouse_provider import (
    greenhouse_provider,
)
from career_agent.services.job_import_service import (
    JobImportService,
)
from career_agent.models.job_search_criteria import JobSearchCriteria
from career_agent.services.job_search_service import JobSearchService
from career_agent.models.enums import RemoteType
from career_agent.models.enums import EmploymentType
from career_agent.models.recommendation_options import (
    RecommendationOptions,
)
from career_agent.workflows.recommendation_workflow import (
    RecommendationWorkflow,
)
from career_agent.models.match_result import MatchResult


def _recommendation_workflow() -> RecommendationWorkflow:

    return RecommendationWorkflow()


app = typer.Typer(no_args_is_help=True)


@app.command(help="Import jobs from an ATS provider.")
def import_jobs(
    board: str = typer.Argument(
        ...,
        help="Greenhouse board name",
    ),
):
    service = JobImportService(
        provider=greenhouse_provider(),
    )
    
    result = service.import_jobs(
        board,
    )
    

    typer.echo(f"New: {len(result.new_jobs)}")
    typer.echo(f"Updated: {len(result.updated_jobs)}")
    typer.echo(f"Removed: {len(result.removed_jobs)}")
    typer.echo(f"Unchanged: {len(result.unchanged_jobs)}")


@app.command(help="Search imported job offers.")
def search(
    company: str | None = typer.Option(
        None,
        "--company",
        help="Filter by company name",
    ),
    keyword: str | None = typer.Option(
        None,
        "--keyword",
        help="Search in title and description",
    ),
    location: str | None = typer.Option(
        None,
        "--location",
        help="Filter by location",
    ),
    remote: str | None = typer.Option(
        None,
        "--remote",
        help="Filter by remote type",
    ),
    employment: str | None = typer.Option(
        None,
        "--employment",
        help="Filter by employment type",
    ),
    page: int = typer.Option(
        1,
        "--page",
        min=1,
        help="Page number",
    ),
):
    criteria = _build_search_criteria(
        company,
        location,
        keyword,
        remote,
        employment,
        page,
    )
    service = JobSearchService()

    jobs = service.search(criteria)

    typer.echo(f"Found {len(jobs)} jobs")
    
    typer.echo()

    _print_jobs(jobs)
    
@app.command(
    help="Recommend jobs for the current candidate profile.",
)
def recommend(
    limit: int = typer.Option(
        10,
        "--limit",
        min=1,
        help="Maximum number of recommendations",
    ),
    min_score: float = typer.Option(
        0.0,
        "--min-score",
        min=0.0,
        max=1.0,
        help="Minimum recommendation score",
    ),
):

    workflow = _recommendation_workflow()

    results = workflow.execute(
        RecommendationOptions(
            limit=limit,
            min_score=min_score,
        ),
    )
    for result in results:

        _print_match_result(
            result,
        )
    
def _print_match_result(
    result: MatchResult,
) -> None:

    typer.echo(
        result.job.title,
    )

    typer.echo(
        result.job.company_name,
    )

    typer.echo(
        result.job.location,
    )
    
    typer.echo(
        result.job.url,
    )

    typer.echo()

    typer.echo(
        f"Score: {result.score:.0%}",
    )

    if result.matched_requirements:

        typer.echo("Matched:")

        for requirement in result.matched_requirements:

            typer.echo(
                f"  ✓ {requirement}",
            )

    if result.missing_requirements:

        typer.echo("Missing:")

        for requirement in result.missing_requirements:

            typer.echo(
                f"  ✗ {requirement}",
            )

    typer.echo()

def _build_search_criteria(
    company: str | None,
    location: str | None,
    keyword: str | None,
    remote: str | None,
    employment: str | None,
    page: int,
) -> JobSearchCriteria:

    return JobSearchCriteria(
        company_name=company,
        location=location,
        keywords=[keyword] if keyword else [],
        remote_type=(
            RemoteType(remote)
            if remote
            else None
        ),
        employment_type=(
            EmploymentType(employment)
            if employment
            else None
        ),
        page=page,
    )
    
def _print_jobs(
    jobs,
) -> None:

    for job in jobs:
        typer.echo(job.title)
        typer.echo(f"  Company : {job.company_name}")
        typer.echo(f"  Location: {job.location}")
        typer.echo(f"  URL     : {job.url}")
        typer.echo("-" * 80)

if __name__ == "__main__":
    app()