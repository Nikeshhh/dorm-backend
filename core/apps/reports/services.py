from django.http import HttpResponse
from django.shortcuts import render


def get_report_file_reponse(
    request,
    context: dict,
    template_name: str,
    base_filename: str,
    filename_postfix: str,
) -> HttpResponse:
    document_content = render(
        request=request,
        template_name=template_name,
        context=context,
    ).content
    response = HttpResponse(document_content, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="{base_filename}_{filename_postfix}.html"'
    )
    return response
