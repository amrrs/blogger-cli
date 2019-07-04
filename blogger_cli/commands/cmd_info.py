from itertools import zip_longest

import click
from blogger_cli.cli import pass_context


@click.command('info', short_help="Show blog's properties")
@click.argument('blog', required=False)
@click.option('-v', '--verbose', is_flag=True)
@pass_context
def cli(ctx, blog, verbose):
    """
    Get details about blogs and app itself\n
    Usage:\n
    bloggger info\n
    blogger info <blogname>
    """
    ctx.verbose = verbose
    blog_exists = ctx.blog_exists(blog)

    if blog and not blog_exists:
        ctx.log('Invalid blog name. No such blog', blog)

    elif not blog:
        # List all blogs
        ctx.log("\nRegistered Blogs:")
        for i in ctx.blog_list:
            default = ctx.default_blog
            ctx.log('  ', i) if i != default else ctx.log('  ', i, '[default]')
        if len(ctx.blog_list) == 0:
            ctx.log(' ', "No blog registered yet!")

        ctx.log("\nBlog:configs [standard] \tOptional:configs [Advanced]")
        for i, j in zip_longest(ctx.config_keys, ctx.optional_config):
            j = j if j else " "
            ctx.log('  ', i, '\t\t', j)

        ctx.log("\nTip: Use blogger info blogname for blog details")

    else:
        if blog == ctx.default_blog:
            ctx.log("\nBlog Name:", blog, '[Default]')
        else:
            ctx.log("\nBlog Name:", blog)

        ctx.log('Configurations:')
        blog_dict = ctx.config.read(blog)
        for k, v in sorted(blog_dict.items()):
            ctx.log('  ', k, "->",  v)
