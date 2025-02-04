import os
from shutil import copyfile, SameFileError
from urllib.request import urlopen, Request

import markdown
from bs4 import BeautifulSoup as BS

from blogger_cli.converter.extractor import (
    extract_main_and_meta_from_file_content, extract_topic,
    extract_and_write_static, replace_ext
    )


def convert_and_copy_to_blog(ctx, md_file):
    md_file_path = os.path.abspath(os.path.expanduser(md_file))
    html_body, meta = convert(ctx, md_file_path)
    html_filename_meta = write_html_and_md(ctx, html_body,
                                            md_file_path, meta)
    return html_filename_meta


def convert(ctx, md_file_path):
    with open(md_file_path, 'r', encoding='utf8') as rf:
        md_data = rf.read()

    ctx.vlog(":: Extracting meta info")
    main_md, metadata = extract_main_and_meta_from_file_content(ctx, md_data)
    extensions = ['extra', 'smarty']
    html = markdown.markdown(main_md, extensions=extensions,
                            output_format='html5')
    return html, metadata


def write_html_and_md(ctx, html_body, md_file_path, meta):
    md_filename = os.path.basename(md_file_path)
    destination_dir = ctx.conversion['destination_dir']
    override_meta = ctx.conversion['override_meta']
    topic = extract_topic(ctx, meta)

    md_filename = os.path.join(topic, md_filename)
    html_filename = replace_ext(md_filename, '.html')
    html_file_path = os.path.join(destination_dir, html_filename)
    new_md_file_path = os.path.join(destination_dir, md_filename)
    new_blog_post_dir = os.path.dirname(html_file_path)
    ctx.vlog(":: New blog_posts_dir finalized", new_blog_post_dir)

    if not os.path.exists(new_blog_post_dir):
        os.mkdir(new_blog_post_dir)

    extract_static = ctx.conversion['extract_static']
    if extract_static:
        html_body = extract_and_write_static(ctx, html_body, new_blog_post_dir,
                                            md_filename)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        ctx.log(":: Converted basic html to", html_file_path)

    try:
        copyfile(md_file_path, new_md_file_path)
        ctx.log(":: Copied md file to", new_md_file_path)
    except  SameFileError:
        os.remove(new_md_file_path)
        copyfile(md_file_path, new_md_file_path)
        ctx.log(":: Overwriting md file", new_md_file_path)

    return (html_filename, meta)
