# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from .lib.generate_images import generate_gradients, get_gradient_direction, generate_base64_image, resize_image

def render():
    images = []

    avatar = st.file_uploader("User/Company logo", help="Recommended size: 90x90 pixels", key="avatar")
    if avatar != None:
        images.append(avatar)

    image1 = st.file_uploader("Choose front image", help="Recommended size: 1200x780 pixels", key="image2")
    if image1 != None:
        images.append(image1)

    image2 = st.file_uploader("Choose bottom image", help="Recommended size: 1200x780 pixels", key="image1")
    if image2 != None:
        images.append(image2)

    direction = st.selectbox(
        'Gradient direction',
        ['0 degrees',
        '45 degrees',
        '90 degrees',
        '135 degrees',
        '180 degrees',
        '225 degrees',
        '270 degrees',
        '315 degrees'
        ],
    )

    showCategory = st.checkbox('Show category text and icon')

    color = st.color_picker('Category text color', '#262730', help="Make sure the color is from our palette")

    return [images, showCategory, direction, color]

def generate(images, category, gradient_direction, color):
    verify_arguments(images)

    # Get image byte data, resize and generate the base64 encoded version
    buffered_avatar = resize_image(images[0], 90, 90)
    buffered_image1 = resize_image(images[1], 1200, 780)
    buffered_image2 = resize_image(images[2], 1200, 780)
    avatar = generate_base64_image(buffered_avatar.getvalue())
    bottom_image = generate_base64_image(buffered_image1.getvalue())
    front_image = generate_base64_image(buffered_image2.getvalue())
    categoryContent = ''

    generated_images = []
    gradients = generate_gradients()
    coordinates = get_gradient_direction(gradient_direction)

    for i in range(len(gradients) - 1):

        if category:
            categoryContent = f"""
            <path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd" d="M90 48C66.804 48 48 67.0279 48 90.5C48 113.972 66.804 133 90 133H248C271.196 133 290 113.972 290 90.5C290 67.0279 271.196 48 248 48H90ZM89.5 60.1429C73.2076 60.1429 60 73.5077 60 89.994C60 106.48 73.2076 119.845 89.5 119.845H90.5C106.792 119.845 120 106.48 120 89.994C120 73.5077 106.792 60.1429 90.5 60.1429H89.5Z" fill="white"/>
            
            # Circle image
            <circle cx="90" cy="90" r="30" fill="url(#avatar-image)"/>

            # Case Study Text
            <path d="M148.662 86.9347H145.474C145.383 86.4119 145.216 85.9489 144.972 85.5455C144.727 85.1364 144.423 84.7898 144.06 84.5057C143.696 84.2216 143.281 84.0085 142.815 83.8665C142.355 83.7188 141.858 83.6449 141.324 83.6449C140.375 83.6449 139.534 83.8835 138.801 84.3608C138.068 84.8324 137.494 85.5256 137.079 86.4403C136.665 87.3494 136.457 88.4602 136.457 89.7727C136.457 91.108 136.665 92.233 137.079 93.1477C137.5 94.0568 138.074 94.7443 138.801 95.2102C139.534 95.6705 140.372 95.9006 141.315 95.9006C141.838 95.9006 142.327 95.8324 142.781 95.696C143.241 95.554 143.653 95.3466 144.017 95.0739C144.386 94.8011 144.696 94.4659 144.946 94.0682C145.202 93.6705 145.378 93.2159 145.474 92.7046L148.662 92.7216C148.543 93.5511 148.284 94.3296 147.886 95.0568C147.494 95.7841 146.98 96.4261 146.344 96.983C145.707 97.5341 144.963 97.9659 144.111 98.2784C143.258 98.5852 142.312 98.7386 141.273 98.7386C139.739 98.7386 138.369 98.3835 137.165 97.6733C135.96 96.9631 135.011 95.9375 134.318 94.5966C133.625 93.2557 133.278 91.6477 133.278 89.7727C133.278 87.8921 133.628 86.2841 134.327 84.9489C135.025 83.608 135.977 82.5824 137.182 81.8722C138.386 81.1619 139.75 80.8068 141.273 80.8068C142.244 80.8068 143.148 80.9432 143.983 81.2159C144.818 81.4886 145.562 81.8892 146.216 82.4176C146.869 82.9403 147.406 83.5824 147.827 84.3438C148.253 85.0994 148.531 85.9631 148.662 86.9347Z" fill="{color}"/>
            <path d="M155.428 98.7642C154.599 98.7642 153.851 98.6165 153.187 98.321C152.528 98.0199 152.005 97.5767 151.618 96.9915C151.238 96.4063 151.047 95.6847 151.047 94.8267C151.047 94.0881 151.184 93.4773 151.457 92.9943C151.729 92.5114 152.101 92.125 152.573 91.8352C153.045 91.5455 153.576 91.3267 154.167 91.179C154.763 91.0256 155.38 90.9148 156.016 90.8466C156.783 90.7671 157.405 90.696 157.883 90.6335C158.36 90.5653 158.707 90.4631 158.922 90.3267C159.144 90.1847 159.255 89.9659 159.255 89.6705V89.6193C159.255 88.9773 159.064 88.4801 158.684 88.1278C158.303 87.7756 157.755 87.5994 157.039 87.5994C156.283 87.5994 155.684 87.7642 155.241 88.0938C154.803 88.4233 154.508 88.8125 154.354 89.2614L151.474 88.8523C151.701 88.0568 152.076 87.3921 152.599 86.858C153.121 86.3182 153.761 85.9148 154.516 85.6477C155.272 85.375 156.107 85.2386 157.022 85.2386C157.653 85.2386 158.28 85.3125 158.905 85.4602C159.53 85.608 160.101 85.8523 160.618 86.1932C161.136 86.5284 161.55 86.9858 161.863 87.5653C162.181 88.1449 162.34 88.8693 162.34 89.7386V98.5H159.374V96.7017H159.272C159.084 97.0653 158.82 97.4063 158.479 97.7244C158.144 98.0369 157.721 98.2898 157.209 98.483C156.704 98.6705 156.11 98.7642 155.428 98.7642ZM156.229 96.4972C156.849 96.4972 157.386 96.375 157.84 96.1307C158.295 95.8807 158.644 95.5511 158.888 95.1421C159.138 94.733 159.263 94.2869 159.263 93.804V92.2614C159.167 92.3409 159.002 92.4148 158.769 92.483C158.542 92.5511 158.286 92.6108 158.002 92.6619C157.718 92.7131 157.437 92.7585 157.158 92.7983C156.88 92.8381 156.638 92.8722 156.434 92.9006C155.974 92.9631 155.562 93.0653 155.198 93.2074C154.834 93.3494 154.547 93.5483 154.337 93.804C154.127 94.054 154.022 94.3778 154.022 94.7756C154.022 95.3438 154.229 95.7727 154.644 96.0625C155.059 96.3523 155.587 96.4972 156.229 96.4972Z" fill="{color}"/>
            <path d="M176.029 88.8693L173.216 89.1761C173.137 88.8921 172.998 88.625 172.799 88.375C172.606 88.125 172.344 87.9233 172.015 87.7699C171.685 87.6165 171.282 87.5398 170.804 87.5398C170.162 87.5398 169.623 87.679 169.185 87.9574C168.753 88.2358 168.54 88.5966 168.546 89.0398C168.54 89.4205 168.679 89.7301 168.964 89.9688C169.253 90.2074 169.731 90.4034 170.395 90.5568L172.628 91.0341C173.867 91.3011 174.787 91.7244 175.39 92.304C175.998 92.8835 176.304 93.6421 176.31 94.5796C176.304 95.4034 176.063 96.1307 175.586 96.7614C175.114 97.3864 174.458 97.875 173.617 98.2273C172.776 98.5796 171.81 98.7557 170.719 98.7557C169.117 98.7557 167.827 98.4205 166.85 97.75C165.873 97.0739 165.29 96.1335 165.103 94.929L168.111 94.6392C168.248 95.2301 168.537 95.6761 168.981 95.9773C169.424 96.2784 170.001 96.429 170.711 96.429C171.444 96.429 172.032 96.2784 172.475 95.9773C172.924 95.6761 173.148 95.304 173.148 94.8608C173.148 94.4858 173.003 94.1761 172.714 93.9318C172.429 93.6875 171.986 93.5 171.384 93.3693L169.151 92.9006C167.895 92.6392 166.966 92.1989 166.364 91.5796C165.762 90.9546 165.464 90.1648 165.469 89.2102C165.464 88.4034 165.682 87.7046 166.126 87.1136C166.574 86.5171 167.197 86.0568 167.992 85.733C168.793 85.4034 169.716 85.2386 170.762 85.2386C172.296 85.2386 173.503 85.5653 174.384 86.2188C175.27 86.8722 175.819 87.7557 176.029 88.8693Z" fill="{color}"/>
            <path d="M184.89 98.7557C183.577 98.7557 182.444 98.483 181.489 97.9375C180.54 97.3864 179.81 96.608 179.299 95.6023C178.787 94.5909 178.532 93.4006 178.532 92.0313C178.532 90.6847 178.787 89.5028 179.299 88.4858C179.816 87.4631 180.537 86.6676 181.464 86.0994C182.39 85.5256 183.478 85.2386 184.728 85.2386C185.535 85.2386 186.296 85.3693 187.012 85.6307C187.733 85.8864 188.37 86.2841 188.921 86.8239C189.478 87.3636 189.915 88.0511 190.233 88.8864C190.552 89.7159 190.711 90.7046 190.711 91.8523V92.7983H179.981V90.7188H187.753C187.748 90.1278 187.62 89.6023 187.37 89.1421C187.12 88.6761 186.77 88.3097 186.321 88.0426C185.878 87.7756 185.361 87.6421 184.77 87.6421C184.14 87.6421 183.586 87.7955 183.108 88.1023C182.631 88.4034 182.259 88.8011 181.992 89.2955C181.731 89.7841 181.597 90.321 181.591 90.9063V92.7216C181.591 93.483 181.731 94.1364 182.009 94.6818C182.287 95.2216 182.677 95.6364 183.177 95.9261C183.677 96.2102 184.262 96.3523 184.932 96.3523C185.381 96.3523 185.787 96.2898 186.151 96.1648C186.515 96.0341 186.83 95.8438 187.097 95.5938C187.364 95.3438 187.566 95.0341 187.702 94.6648L190.583 94.9886C190.401 95.75 190.054 96.4148 189.543 96.983C189.037 97.5455 188.39 97.983 187.6 98.2955C186.81 98.6023 185.907 98.7557 184.89 98.7557Z" fill="{color}"/>
            <path d="M210.1 88.8693L207.288 89.1761C207.208 88.8921 207.069 88.625 206.87 88.375C206.677 88.125 206.416 87.9233 206.086 87.7699C205.757 87.6165 205.353 87.5398 204.876 87.5398C204.234 87.5398 203.694 87.679 203.257 87.9574C202.825 88.2358 202.612 88.5966 202.618 89.0398C202.612 89.4205 202.751 89.7301 203.035 89.9688C203.325 90.2074 203.802 90.4034 204.467 90.5568L206.7 91.0341C207.939 91.3011 208.859 91.7244 209.461 92.304C210.069 92.8835 210.376 93.6421 210.382 94.5796C210.376 95.4034 210.135 96.1307 209.657 96.7614C209.186 97.3864 208.529 97.875 207.689 98.2273C206.848 98.5796 205.882 98.7557 204.791 98.7557C203.189 98.7557 201.899 98.4205 200.921 97.75C199.944 97.0739 199.362 96.1335 199.174 94.929L202.183 94.6392C202.319 95.2301 202.609 95.6761 203.052 95.9773C203.495 96.2784 204.072 96.429 204.782 96.429C205.515 96.429 206.103 96.2784 206.546 95.9773C206.995 95.6761 207.22 95.304 207.22 94.8608C207.22 94.4858 207.075 94.1761 206.785 93.9318C206.501 93.6875 206.058 93.5 205.456 93.3693L203.223 92.9006C201.967 92.6392 201.038 92.1989 200.436 91.5796C199.833 90.9546 199.535 90.1648 199.541 89.2102C199.535 88.4034 199.754 87.7046 200.197 87.1136C200.646 86.5171 201.268 86.0568 202.064 85.733C202.865 85.4034 203.788 85.2386 204.833 85.2386C206.368 85.2386 207.575 85.5653 208.456 86.2188C209.342 86.8722 209.89 87.7557 210.1 88.8693Z" fill="{color}"/>
            <path d="M219.703 85.4091V87.7955H212.177V85.4091H219.703ZM214.035 82.2727H217.12V94.5625C217.12 94.9773 217.183 95.2955 217.308 95.5171C217.438 95.733 217.609 95.8807 217.819 95.9602C218.029 96.0398 218.262 96.0796 218.518 96.0796C218.711 96.0796 218.887 96.0653 219.046 96.0369C219.211 96.0085 219.336 95.983 219.421 95.9602L219.941 98.3722C219.777 98.429 219.541 98.4915 219.234 98.5597C218.933 98.6278 218.563 98.6676 218.126 98.679C217.353 98.7017 216.657 98.5852 216.038 98.3296C215.419 98.0682 214.927 97.6648 214.563 97.1193C214.206 96.5739 214.029 95.8921 214.035 95.0739V82.2727Z" fill="{color}"/>
            <path d="M230.867 92.9943V85.4091H233.952V98.5H230.96V96.1733H230.824C230.529 96.9063 230.043 97.5057 229.367 97.9716C228.696 98.4375 227.87 98.6705 226.887 98.6705C226.029 98.6705 225.27 98.4801 224.611 98.0994C223.958 97.7131 223.446 97.1534 223.077 96.4205C222.708 95.6818 222.523 94.7898 222.523 93.7443V85.4091H225.608V93.2671C225.608 94.0966 225.835 94.7557 226.29 95.2443C226.745 95.733 227.341 95.9773 228.08 95.9773C228.534 95.9773 228.975 95.8665 229.401 95.6449C229.827 95.4233 230.176 95.0938 230.449 94.6563C230.727 94.2131 230.867 93.6591 230.867 92.9943Z" fill="{color}"/>
            <path d="M242.222 98.7301C241.194 98.7301 240.274 98.4659 239.461 97.9375C238.649 97.4091 238.007 96.6421 237.535 95.6364C237.063 94.6307 236.828 93.4091 236.828 91.9716C236.828 90.5171 237.066 89.2898 237.543 88.2898C238.026 87.2841 238.677 86.5256 239.495 86.0142C240.313 85.4972 241.225 85.2386 242.231 85.2386C242.998 85.2386 243.629 85.3693 244.123 85.6307C244.617 85.8864 245.009 86.196 245.299 86.5597C245.589 86.9176 245.813 87.2557 245.972 87.5739H246.1V81.0455H249.194V98.5H246.16V96.4375H245.972C245.813 96.7557 245.583 97.0938 245.282 97.4517C244.981 97.804 244.583 98.1051 244.089 98.3551C243.595 98.6051 242.972 98.7301 242.222 98.7301ZM243.083 96.1989C243.737 96.1989 244.293 96.0227 244.754 95.6705C245.214 95.3125 245.563 94.8153 245.802 94.179C246.041 93.5426 246.16 92.8011 246.16 91.9546C246.16 91.108 246.041 90.3722 245.802 89.7472C245.569 89.1222 245.222 88.6364 244.762 88.2898C244.308 87.9432 243.748 87.7699 243.083 87.7699C242.396 87.7699 241.822 87.9489 241.362 88.3068C240.901 88.6648 240.555 89.1591 240.322 89.7898C240.089 90.4205 239.972 91.1421 239.972 91.9546C239.972 92.7727 240.089 93.5028 240.322 94.1449C240.561 94.7813 240.91 95.2841 241.37 95.6534C241.836 96.0171 242.407 96.1989 243.083 96.1989Z" fill="{color}"/>
            <path d="M254.639 103.409C254.219 103.409 253.83 103.375 253.472 103.307C253.119 103.244 252.838 103.17 252.628 103.085L253.344 100.682C253.793 100.813 254.193 100.875 254.546 100.869C254.898 100.864 255.207 100.753 255.475 100.537C255.747 100.327 255.977 99.9744 256.165 99.4801L256.429 98.7727L251.682 85.4091H254.955L257.972 95.2955H258.108L261.134 85.4091H264.415L259.173 100.085C258.929 100.778 258.605 101.372 258.202 101.866C257.798 102.366 257.304 102.747 256.719 103.009C256.139 103.276 255.446 103.409 254.639 103.409Z" fill="{color}"/>
        """

        generated_images.append(f"""
            <svg width="1480" height="700" viewBox="0 0 1480 700" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                # Group to hold the background colors 
                <g clip-path="url(#clip0_418_273)">
                    # White background
                    <rect width="1480" height="700" fill="white"/>
                    # Gradient
                    <rect width="1480" height="700" fill="url(#gradient)"/>

                    # Left browser
                    <g filter="url(#filter0_d_418_273)">
                        <g filter="url(#filter1_dd_418_273)">
                            # Image
                            <rect x="520" y="315" width="100%" height="100%" fill="url(#image-1)"/>

                            <path fill-rule="evenodd" clip-rule="evenodd" d="M505 238C498.373 238 493 243.373 493 250V700H527C523.686 700 521 697.314 521 694V320C521 316.686 523.686 314 527 314H1227C1230.31 314 1233 316.686 1233 320V238H505ZM1233 694C1233 697.314 1230.31 700 1227 700H1233V694Z" fill="white"/>
                            <path d="M492.5 700V700.5H493H527V700V699.5C523.962 699.5 521.5 697.038 521.5 694V320C521.5 316.962 523.962 314.5 527 314.5H1227C1230.04 314.5 1232.5 316.962 1232.5 320H1233H1233.5V238V237.5H1233H505C498.096 237.5 492.5 243.096 492.5 250V700ZM1233 700.5H1233.5V700V694H1233H1232.5C1232.5 697.038 1230.04 699.5 1227 699.5V700V700.5H1233Z" stroke="#FAFAFA"/>
                        </g>
                        <circle cx="527" cy="276" r="6" fill="#FF6C6C"/>
                        <circle cx="555" cy="276" r="6" fill="#FFE312"/>
                        <circle cx="583" cy="276" r="6" fill="#3DD56D"/>
                    </g>

                    # Right browser
                    <g filter="url(#filter2_d_418_273)">
                        <g filter="url(#filter3_dd_418_273)">
                            # Image
                            <rect xmlns="http://www.w3.org/2000/svg" x="765" y="239" width="718" height="461" rx="6" fill="url(#image-2)"/>

                            <path fill-rule="evenodd" clip-rule="evenodd" d="M752 162C745.373 162 740 167.373 740 174V700H768V246C768 241.582 771.582 238 776 238H1480V162H752Z" fill="white"/>
                            <path d="M739.5 700V700.5H740H768H768.5V700V246C768.5 241.858 771.858 238.5 776 238.5H1480H1480.5V238V162V161.5H1480H752C745.096 161.5 739.5 167.096 739.5 174V700Z" stroke="#FAFAFA"/>
                        </g>
                        <circle cx="774" cy="200" r="6" fill="#FF6C6C"/>
                        <circle cx="802" cy="200" r="6" fill="#FFE312"/>
                        <circle cx="830" cy="200" r="6" fill="#3DD56D"/>
                    </g>
                </g>

                # Category text and icon
                {categoryContent}

                <defs>
                    # Patterns for images
                    <pattern id="avatar-image" patternContentUnits="userSpaceOnUse" width="100%" height="100%">
                        <image id="image-avatar" width="60" height="60" xlink:href="data:image/jpeg;charset=utf-8;base64,{avatar}" />
                    </pattern>
                    <pattern id="image-1" patternContentUnits="userSpaceOnUse" width="100%" height="100%">
                        <image id="screenshot-1" x="0" y="0" width="1200" height="780" xlink:href="data:image/jpeg;charset=utf-8;base64,{front_image}" />
                    </pattern>
                    <pattern id="image-2" patternContentUnits="userSpaceOnUse" width="100%" height="100%">
                        <image id="screenshot-2" x="0" y="0" width="1200" height="780" xlink:href="data:image/jpeg;charset=utf-8;base64,{bottom_image}" />
                    </pattern>

                    # Filters and such
                    <filter id="filter0_d_418_273" x="452" y="201" width="806" height="528" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                        <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                        <feOffset dx="-8" dy="-4"/>
                        <feGaussianBlur stdDeviation="16"/>
                        <feComposite in2="hardAlpha" operator="out"/>
                        <feColorMatrix type="matrix" values="0 0 0 0 0.960784 0 0 0 0 0.921569 0 0 0 0 1 0 0 0 0.16 0"/>
                        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_418_273"/>
                        <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_418_273" result="shape"/>
                    </filter>
                    <filter id="filter1_dd_418_273" x="452" y="202" width="822" height="544" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                        <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                        <feOffset dy="2"/>
                        <feGaussianBlur stdDeviation="6"/>
                        <feComposite in2="hardAlpha" operator="out"/>
                        <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0.258824 0 0 0 0 0.501961 0 0 0 0.05 0"/>
                        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_418_273"/>
                        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                        <feOffset dy="5"/>
                        <feGaussianBlur stdDeviation="20"/>
                        <feComposite in2="hardAlpha" operator="out"/>
                        <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0.258824 0 0 0 0 0.501961 0 0 0 0.25 0"/>
                        <feBlend mode="normal" in2="effect1_dropShadow_418_273" result="effect2_dropShadow_418_273"/>
                        <feBlend mode="normal" in="SourceGraphic" in2="effect2_dropShadow_418_273" result="shape"/>
                    </filter>
                    <filter id="filter2_d_418_273" x="699" y="125" width="806" height="604" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                        <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                        <feOffset dx="-8" dy="-4"/>
                        <feGaussianBlur stdDeviation="16"/>
                        <feComposite in2="hardAlpha" operator="out"/>
                        <feColorMatrix type="matrix" values="0 0 0 0 0.960784 0 0 0 0 0.921569 0 0 0 0 1 0 0 0 0.16 0"/>
                        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_418_273"/>
                        <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_418_273" result="shape"/>
                    </filter>
                    <filter id="filter3_dd_418_273" x="699" y="126" width="822" height="620" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                        <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                        <feOffset dy="2"/>
                        <feGaussianBlur stdDeviation="6"/>
                        <feComposite in2="hardAlpha" operator="out"/>
                        <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0.258824 0 0 0 0 0.501961 0 0 0 0.05 0"/>
                        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_418_273"/>
                        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                        <feOffset dy="5"/>
                        <feGaussianBlur stdDeviation="20"/>
                        <feComposite in2="hardAlpha" operator="out"/>
                        <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0.258824 0 0 0 0 0.501961 0 0 0 0.25 0"/>
                        <feBlend mode="normal" in2="effect1_dropShadow_418_273" result="effect2_dropShadow_418_273"/>
                        <feBlend mode="normal" in="SourceGraphic" in2="effect2_dropShadow_418_273" result="shape"/>
                    </filter>

                    <clipPath id="clip0_418_273">
                        <rect width="1480" height="700" fill="white"/>
                    </clipPath>

                    # Gradient
                    <linearGradient id="gradient" x1="{coordinates[0]}" y1="{coordinates[1]}" x2="{coordinates[2]}" y2="{coordinates[3]}">{gradients[i]}</linearGradient>
                </defs>
            </svg>
        """.strip())

    return generated_images


def verify_arguments(images):
    MIN_IMAGES = 3

    if len(images) < MIN_IMAGES:
        st.error("Please add at least three images")
        st.stop()
