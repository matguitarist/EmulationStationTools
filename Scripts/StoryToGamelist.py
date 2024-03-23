import os
import xml.etree.ElementTree as ET

def update_xml(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Folder containing the text files
    txt_folder = "story"
    
    # Folder containing the video files
    video_folder = "videos"

    # Iterate through each <game> element in the XML
    for game in root.findall('.//game'):
        # Get the game name from the <name> tag
        game_name = game.find('name').text

        # Form the corresponding TXT file name
        txt_file_path = os.path.join(txt_folder, f"{game_name}.txt")
        
        # Form the corresponding video file name
        video_file_path = os.path.join(video_folder, f"{game_name}-video.mp4")

        # Check if the TXT file exists
        if os.path.isfile(txt_file_path):
            # Read the content from the TXT file with explicit encoding
            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                desc_content = txt_file.read().strip()

            # Check if <desc> tag already exists, if not, create it
            desc_tag = game.find('desc')
            if desc_tag is None:
                desc_tag = ET.SubElement(game, 'desc')
                print(f"Added <desc> tag for {game_name}")

            # Update the content of the <desc> tag
            desc_tag.text = desc_content
            print(f"Updated <desc> content for {game_name}")

        # Check if the video file exists
        if os.path.isfile(video_file_path):
            # Check if <video> tag already exists, if not, create it
            video_tag = game.find('video')
            if video_tag is None:
                video_tag = ET.SubElement(game, 'video')
                print(f"Added <video> tag for {game_name}")

            # Update the content of the <video> tag
            video_tag.text = f"./{video_folder}/{game_name}-video.mp4"
            print(f"Updated <video> content for {game_name}")

    # Save the updated XML file
    tree.write(xml_file)
    print(f"Updated {xml_file} with new <desc> and <video> content")

if __name__ == "__main__":
    # Assuming the script is in the same folder as gamelist.xml
    gamelist_xml_path = "gamelist.xml"
    
    # Call the function to update the XML
    update_xml(gamelist_xml_path)
