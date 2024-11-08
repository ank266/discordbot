from common import bot
import discord
import sys, os, shutil, subprocess
from settings.read_write_data_storage_files import read_editors

running_processes = {}

@bot.command()
async def create_file(ctx, file_name: str):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    if os.path.exists(file_name):
        await ctx.send(f"`{file_name}` already exists.")
        return

    with open(file_name, 'w') as file:
        file.write("")
    await ctx.send(f"`{file_name}` has been created.")

@bot.command()
async def delete_file(ctx, file_name: str):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    if not os.path.exists(file_name):
        await ctx.send(f"`{file_name}` does not exist.")
        return

    os.remove(file_name)
    await ctx.send(f"`{file_name}` has been deleted.")


@bot.command()
async def view_file(ctx, file_name: str):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return
    
    await ctx.send(file=discord.File(file_name))

@bot.command()
async def append_to_file(ctx, file_name: str, code: str, offset: int = 0):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    # Verify the file exists and is a Python file
    if not os.path.exists(file_name):
        await ctx.send(f"`{file_name}` does not exist.")
        return

    # Read the file content and find the insertion point
    with open(file_name, 'r') as file:
        lines = file.readlines()

    if offset >= 0:
        insert_position = max(0, len(lines) - offset)
    else:
        await ctx.send("Offset cannot be negative.")
        return

    lines.insert(insert_position, code+"\n")

    # Write the modified content back to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)

    await ctx.send(f"Successfully added to `{file_name}` with an offset of {offset} from the end.")


@bot.command()
async def find_all(ctx, file_name: str, pattern: str):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return


    # Split the input into the code and occurrence parts
    parts = pattern.rsplit(' ', 1)
    if len(parts) == 2 and parts[1].isdigit():
        code = parts[0].strip().strip('"')
    elif len(parts) == 2 and parts[1].upper() == "ALL":
        code = parts[0].strip().strip('"')
    else:
        code = pattern.strip().strip('"')

    # Read the content of the file first
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Initialize variables
    count_found = 0

    # Iterate through lines and keep those that do not match the target occurrence
    for line in lines:
        if code.strip() in line.strip():
            count_found += 1
    if count_found == 0:
        await ctx.send(f"No occurrences of `{pattern}` found in the file.")
    else:
        await ctx.send(f"Found {count_found} occurrence(s) of `{pattern}` in the file.")


    
# Find and remove the specified line of code
@bot.command()
async def delete_line(ctx, file_name: str, code_occurrence: str, amount: str):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    if amount == "ALL":
        occurrence = "ALL"
    else:
        occurrence = int(amount)

    # Read the content of the file first
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Initialize variables
    count_found = 0
    lines_to_keep = []

    # Iterate through lines and keep those that do not match the target occurrence
    for line in lines:
        if code_occurrence.strip() in line.strip():
            count_found += 1
            if occurrence == "ALL" or count_found == occurrence:
                continue  # Skip this line, effectively deleting it
        lines_to_keep.append(line)

    if count_found == 0:
        await ctx.send("No such line found in the file.")
    elif occurrence != "ALL" and count_found < occurrence:
        await ctx.send(f"There are only {count_found} occurrences of this line. Please specify a valid occurrence number.")
    else:
        # Write the modified content back to the file
        with open(file_name, 'w') as file:
            file.writelines(lines_to_keep)
        await ctx.send(f"Occurrence number {occurrence} of the line has been successfully deleted." if occurrence != "ALL" else "All instances of the line have been successfully deleted.")

@bot.command()
async def replace(ctx, file_name: str, before: str, after: str, occurrence: str = "1"):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    # Read the content of the file first
    with open(file_name, 'r') as file:
        lines = file.readlines()

    count_found = 0
    updated_lines = []

    try:
        if occurrence.isdigit():
            occurrence = int(occurrence)
        elif occurrence.upper() == "ALL":
            occurrence = "ALL"
        else:
            raise ValueError("Invalid occurrence parameter.")
    except ValueError:
        await ctx.send("Invalid occurrence parameter. Use a number or 'ALL'.")
        return

    # Replace the specified pattern with the new pattern
    for line in lines:
        if before.strip() in line.strip():
            count_found += 1
            if occurrence == "ALL" or count_found == occurrence:
                updated_lines.append(line.replace(before, after))
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    with open(file_name, 'w') as file:
        file.writelines(updated_lines)

    if count_found == 0:
        await ctx.send(f"No occurrences of `{before}` found in the file.")
    elif occurrence == "ALL":
        await ctx.send(f"Successfully replaced all occurrences of `{before}` with `{after}`.")
    elif count_found < occurrence:
        await ctx.send(f"There are only {count_found} occurrences of `{before}`. Please specify a valid occurrence number.")
    else:
        await ctx.send(f"Successfully replaced occurrence number {occurrence} of `{before}` with `{after}`.")




@bot.command()
async def upload_file(ctx, *, force: str = ''):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    # Determine if force upload is enabled
    force_upload = (force.strip().lower() == 'f')

    if ctx.message.attachments:
        response_messages = []
        for attachment in ctx.message.attachments:
            file_path = attachment.filename
            # Check if the file already exists
            if os.path.exists(file_path) and not force_upload:
                response_messages.append(f"File '{file_path}' already exists. Use `$upload f` to overwrite.")
            else:
                # Save the attachment, overwriting if force_upload is True
                await attachment.save(file_path)
                response_messages.append(f"Saved attachment to {file_path}")
        for message in response_messages:
            await ctx.send(message)
    else:
        await ctx.send("No attachments found in the message.")




@bot.command()
async def rc(ctx, *, command: str):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        output_message = ""
        if stdout:
            output_message += f"**Output:**\n```\n{stdout.strip()}\n```"
        if stderr:
            output_message += f"\n**Errors:**\n```\n{stderr.strip()}\n```"

        if len(output_message) > 2000:
            # Write the output to a file
            output_file_path = "command_output.txt"
            with open(output_file_path, "w") as output_file:
                output_file.write(stdout)
                output_file.write("\n")
                output_file.write(stderr)

            # Send the file as an attachment
            await ctx.send("The output is too long to display. Here is the output file:", file=discord.File(output_file_path))

            # Clean up the file after sending
            os.remove(output_file_path)
        else:
            if not output_message.strip():
                output_message = "The command executed successfully with no output."
            await ctx.send(output_message)
    except Exception as e:
        await ctx.send(f"Failed to execute command: {e}")

        

@bot.command()
async def stop(ctx, file_name: str):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await ctx.send("Not Authorized.")
        return

    process = running_processes.get(file_name)
    if process and process.poll() is None:  # Check if the process is still running
        process.terminate()
        process.wait()  # Wait for the process to terminate
        del running_processes[file_name]  # Remove from tracking
        await ctx.send(f"Process for file `{file_name}` has been stopped.")
    else:
        await ctx.send(f"No running process found for file `{file_name}`.")