import typer
from career_agent.providers.greenhouse_provider import (
    greenhouse_provider,
)
from career_agent.services.job_import_service import (
    JobImportService,
)
from career_agent.models.job_search_criteria import JobSearchCriteria
from career_agent.services.job_search_service import JobSearchService
from career_agent.models.enums import RemoteType


app = typer.Typer(no_args_is_help=True)


@app.command()
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


@app.command()
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
):
    criteria = _build_search_criteria(
        company,
        location,
        keyword,
        remote,
    )
    service = JobSearchService()

    jobs = service.search(criteria)

    typer.echo(f"Found {len(jobs)} jobs")
    
    typer.echo()

    _print_jobs(jobs)

def _build_search_criteria(
    company: str | None,
    location: str | None,
    keyword: str | None,
    remote: str | None,
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