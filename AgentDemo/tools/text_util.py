import re


def is_chinese(text: str) -> bool:
    return not text.isascii()


def is_digit_or_alpha_or_punctuation(char: str) -> bool:
    return char.isalnum() or char in '.,;:!?\'"()[]{}-_/'


def split_chinese_by_length(s: str, target_length: int) -> list[str]:
    current_line = []
    results: list[str] = []
    current_length = 0
    punctuation = '，。、；：！？》）”0123456789.元日年月'
    
    for char in s:
        if current_length >= target_length:
            if char in punctuation:
                current_line.append(char)
                current_length += 1
                continue
            results.append(''.join(current_line))
            current_line = []
            current_length = 0
        
        current_length += 1
        current_line.append(char)
    
    if current_line:
        results.append(''.join(current_line))
    
    return results


def split_english_by_length(s: str, target_length: int = 70) -> list[str]:
    words = s.split()
    current_line = []
    results: list[str] = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) > target_length:
            results.append(' '.join(current_line))
            current_line = []
            current_length = 0
        
        current_line.append(word)
        current_length += len(word)
    
    if current_line:
        results.append(' '.join(current_line))
    
    return results


def split_by_length(s: str, chinese_target_len: int, english_target_len) -> list[str]:
    if is_chinese(s):
        return split_chinese_by_length(s, chinese_target_len)
    else:
        return split_english_by_length(s, english_target_len)


def split_by_line_break(s) -> list[str]:
    # 使用正则表达式来分割字符串，保留分隔符
    parts = re.split(r'(\n\n|\n)', s)
    
    # 移除空字符串
    parts = [part for part in parts if part != "\n\n" and part != "\n"]
    
    # 根据具体需求处理分割结果，例如去除分隔符等
    return parts


# def text_generator(text_list: list[str]) -> Generator:
#     y = 0
#     for text in text_list:
#         if is_chinese(text):
#             y += 0.7
#
#     position_generator = (Position(TEXT_INIT_X, TEXT_INIT_Y + i * 0.7) for i in itertools.count())
#
#     raise ValueError("already generate for all text")


if __name__ == '__main__':
    test_line_break_str = "Mike\nlove\n\nLucy"
    assert split_by_line_break(test_line_break_str) == ["Mike", "love", "Lucy"]
    test_split_by_length_str = "麦克。喜欢。鸬鹚。"
    print(split_by_length(test_split_by_length_str, 3, 100))
    
    test_str = "这是一个测试字符串元，，，，包含了很多中文字符！和！一些标点符号。我们将尝试按长度分割这个字符串，确保每一行的开头不为标点符号。"
    result = split_by_length(test_str, 9, 85)
    for i, line in enumerate(result):
        print(f"Line {i + 1}: {line}")
