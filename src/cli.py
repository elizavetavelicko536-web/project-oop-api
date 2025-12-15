import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from annotations.core import ProviderFactory
from annotations.annotator import Annotator, save_results_to_docx


def main(argv=None):
    parser = argparse.ArgumentParser(description='Generate annotations for files using a provider')
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--prompts', nargs='*', default=[])
    parser.add_argument('--provider', choices=['mock', 'gigachat'], default='mock')
    parser.add_argument('--out-dir', default='out')
    parser.add_argument('--combine', action='store_true', default=False,
                        help='Объединить все аннотации в один объект')
    args = parser.parse_args(argv)

    for file in args.files:
        if not os.path.exists(file):
            print(f"Ошибка: файл не найден: {file}")
            return 1
    provider = ProviderFactory.create(args.provider)
    annotator = Annotator(provider=provider)

    annotation_results = annotator(args.files, args.prompts)

    if args.combine and len(annotation_results) > 1:
        combined = annotation_results[0]
        for result in annotation_results[1:]:
            combined += result
        print(f"Объединено {len(annotation_results)} аннотаций в один объект")
        print(f"Итоговый промт: {combined.prompt}")
        print(f"Итоговый текст: {len(combined.text)} символов")
        annotation_results = [combined]

    os.makedirs(args.out_dir, exist_ok=True)
    out_file = os.path.join(args.out_dir, 'annotations.docx')

    save_results_to_docx(annotation_results, out_file)
    print('Saved to', out_file)

    print(f"\nОбработано файлов: {len(annotation_results)}")
    for i, result in enumerate(annotation_results, 1):
        print(f"{i}. {os.path.basename(result.file_name)}: "
              f"{len(result.text)} символов, промт: '{result.prompt[:50]}...'")

    return 0


if __name__ == '__main__':
    exit(main())