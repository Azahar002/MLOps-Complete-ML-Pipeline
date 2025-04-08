import os
import logging
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import nltk

nltk.download('stopwords')
nltk.download('punkt')

# Ensure the "logs" directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Setting up logger
logger = logging.getLogger('data_preprocessing')
logger.setLevel(logging.DEBUG)

if not logger.handlers:  # Prevent duplicate handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_file_path = os.path.join(log_dir, 'data_preprocessing.log')
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def transform_text(text):
    try:
        if not isinstance(text, str):
            logger.warning(f"Skipping non-string: {text} ({type(text)})")
            return ""

        ps = PorterStemmer()
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        tokens = [word for word in tokens if word.isalnum()]
        tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
        tokens = [ps.stem(word) for word in tokens]
        return " ".join(tokens)

    except Exception as e:
        logger.error(f"transform_text failed on input: {text} | Error: {e}")
        return ""


def preprocess_df(df, text_column='text', target_column='target'):
    try:
        logger.info('Preprocessing started.')

        encoder = LabelEncoder()
        df[target_column] = encoder.fit_transform(df[target_column])
        logger.info('Target column encoded.')

        df = df.drop_duplicates(keep='first')
        logger.info('Duplicates removed.')

        for idx, val in df[text_column].items():
            try:
                df.at[idx, text_column] = transform_text(val)
                if idx % 500 == 0:
                    logger.debug(f'Transformed {idx} rows...')
            except Exception as e:
                logger.error(f"Text transformation failed at index {idx} | Error: {e}")

        logger.info('Text column transformed.')
        return df

    except KeyError as e:
        logger.error(f'Column not found: {e}')
        raise
    except Exception as e:
        logger.error(f'An error occurred during preprocessing: {e}')
        raise


def main(text_column='text', target_column='target'):
    try:
        logger.info('Loading raw data...')
        train_data = pd.read_csv('./data/raw/train.csv')
        test_data = pd.read_csv('./data/raw/test.csv')

        train_processed = preprocess_df(train_data, text_column, target_column)
        test_processed = preprocess_df(test_data, text_column, target_column)

        data_path = os.path.join("./data", "interim")
        os.makedirs(data_path, exist_ok=True)

        train_processed.to_csv(os.path.join(data_path, "train_processed.csv"), index=False)
        test_processed.to_csv(os.path.join(data_path, "test_processed.csv"), index=False)

        logger.info(f'Processed data saved to {data_path}')

    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
    except pd.errors.EmptyDataError as e:
        logger.error(f'Empty CSV file: {e}')
    except Exception as e:
        logger.error(f'Processing failed: {e}')
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
import os
import logging
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import nltk

nltk.download('stopwords')
nltk.download('punkt')

# Ensure the "logs" directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Setting up logger
logger = logging.getLogger('data_preprocessing')
logger.setLevel(logging.DEBUG)

if not logger.handlers:  # Prevent duplicate handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_file_path = os.path.join(log_dir, 'data_preprocessing.log')
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def transform_text(text):
    try:
        if not isinstance(text, str):
            logger.warning(f"Skipping non-string: {text} ({type(text)})")
            return ""

        ps = PorterStemmer()
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        tokens = [word for word in tokens if word.isalnum()]
        tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
        tokens = [ps.stem(word) for word in tokens]
        return " ".join(tokens)

    except Exception as e:
        logger.error(f"transform_text failed on input: {text} | Error: {e}")
        return ""


def preprocess_df(df, text_column='text', target_column='target'):
    try:
        logger.info('Preprocessing started.')

        encoder = LabelEncoder()
        df[target_column] = encoder.fit_transform(df[target_column])
        logger.info('Target column encoded.')

        df = df.drop_duplicates(keep='first', subset=[text_column, target_column])
        logger.info('Duplicates removed.')

        df[text_column] = df[text_column].apply(transform_text)
        logger.info('Text column transformed.')
        return df

    except KeyError as e:
        logger.error(f'Column not found: {e}')
        raise
    except Exception as e:
        logger.error(f'An error occurred during preprocessing: {e}')
        raise


def main(text_column='text', target_column='target'):
    try:
        logger.info('Loading raw data...')
        train_data = pd.read_csv('./data/raw/train.csv')
        test_data = pd.read_csv('./data/raw/test.csv')

        train_processed = preprocess_df(train_data, text_column, target_column)
        test_processed = preprocess_df(test_data, text_column, target_column)

        data_path = os.path.join("./data", "interim")
        os.makedirs(data_path, exist_ok=True)

        train_processed.to_csv(os.path.join(data_path, "train_processed.csv"), index=False)
        test_processed.to_csv(os.path.join(data_path, "test_processed.csv"), index=False)

        logger.info(f'Processed data saved to {data_path}')

    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
    except pd.errors.EmptyDataError as e:
        logger.error(f'Empty CSV file: {e}')
    except Exception as e:
        logger.error(f'Processing failed: {e}')
        print(f"Error: {e}")


if __name__ == '__main__':
    main()