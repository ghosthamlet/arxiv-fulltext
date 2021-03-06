"""Tests for :mod:`fulltext.extract."""

from unittest import TestCase, mock

from ..domain import ExtractionTask, ExtractionProduct, ExtractionPlaceholder
from .. import extract
from ..services import pdf


class TestCreateExtractionTask(TestCase):
    """Tests for :funcd:`extract.create_extraction_task`."""

    @mock.patch(f'{extract.__name__}.store.store')
    @mock.patch(f'{extract.__name__}.extract_fulltext.apply_async')
    def test_create_task(self, mock_task_delay, mock_store):
        """Create a new task."""
        id_type = 'arxiv'
        paper_id = '1234.56789'
        pdf_url = f'https://arxiv.org/pdf/{paper_id}'
        task_id = 'fooid123'
        mock_task_delay.return_value = mock.MagicMock(task_id=task_id)
        result = extract.create_extraction_task(paper_id, pdf_url, id_type)

        store_called_with, _ = mock_store.call_args
        self.assertEqual(store_called_with[0], paper_id)
        self.assertEqual(store_called_with[1].task_id, task_id)
        self.assertEqual(result, task_id)

    @mock.patch(f'{extract.__name__}.store.store')
    @mock.patch(f'{extract.__name__}.extract_fulltext.apply_async')
    def test_celery_failed(self, mock_task_delay, mock_store):
        """Celery punted."""
        id_type = 'arxiv'
        paper_id = '1234.56789'
        pdf_url = f'https://arxiv.org/pdf/{paper_id}'
        mock_task_delay.side_effect = RuntimeError

        with self.assertRaises(extract.TaskCreationFailed):
            extract.create_extraction_task(paper_id, pdf_url, id_type)

    @mock.patch(f'{extract.__name__}.store.store')
    @mock.patch(f'{extract.__name__}.extract_fulltext.apply_async')
    def test_store_failed(self, mock_task_delay, mock_store):
        """Could not store a placeholder pointer."""
        id_type = 'arxiv'
        paper_id = '1234.56789'
        pdf_url = f'https://arxiv.org/pdf/{paper_id}'
        mock_store.side_effect = RuntimeError

        with self.assertRaises(extract.TaskCreationFailed):
            extract.create_extraction_task(paper_id, pdf_url, id_type)


class TestGetExtractionTask(TestCase):
    """Tests for :func:`extract.get_extraction_task`."""

    @mock.patch(f'{extract.__name__}.extract_fulltext.AsyncResult')
    def test_get_nonexistant_task(self, mock_AsyncResult):
        """PENDING is used if the task does not exist (we set to SENT)."""
        paper_id = '1234.56789v1'
        mock_AsyncResult.return_value = mock.MagicMock(status='PENDING')
        with self.assertRaises(extract.NoSuchTask):
            extract.get_extraction_task(paper_id, 'arxiv')

    @mock.patch(f'{extract.__name__}.extract_fulltext.AsyncResult')
    def test_get_created_task(self, mock_AsyncResult):
        """We set status to SENT when we create a task."""
        paper_id = '1234.56789v1'
        mock_AsyncResult.return_value = mock.MagicMock(status='SENT')
        task = extract.get_extraction_task(paper_id, 'arxiv')
        self.assertEqual(task.status, ExtractionTask.Statuses.IN_PROGRESS)

    @mock.patch(f'{extract.__name__}.extract_fulltext.AsyncResult')
    def test_get_running_task(self, mock_AsyncResult):
        """STARTED status means the task is running."""
        paper_id = '1234.56789v1'
        mock_AsyncResult.return_value = mock.MagicMock(status='STARTED')
        task = extract.get_extraction_task(paper_id, 'arxiv')
        self.assertEqual(task.status, ExtractionTask.Statuses.IN_PROGRESS)

    @mock.patch(f'{extract.__name__}.extract_fulltext.AsyncResult')
    def test_get_retrying_task(self, mock_AsyncResult):
        """RETRY status means the task is being retried as configured."""
        paper_id = '1234.56789v1'
        mock_AsyncResult.return_value = mock.MagicMock(status='RETRY')
        task = extract.get_extraction_task(paper_id, 'arxiv')
        self.assertEqual(task.status, ExtractionTask.Statuses.IN_PROGRESS)

    @mock.patch(f'{extract.__name__}.extract_fulltext.AsyncResult')
    def test_get_failed_task(self, mock_AsyncResult):
        """FAILURE is final."""
        paper_id = '1234.56789v1'
        mock_AsyncResult.return_value = mock.MagicMock(
            status='FAILURE',
            result='utter failure'
        )
        task = extract.get_extraction_task(paper_id, 'arxiv')
        self.assertEqual(task.status, ExtractionTask.Statuses.FAILED)

    @mock.patch(f'{extract.__name__}.extract_fulltext.AsyncResult')
    def test_get_succeeded_task(self, mock_AsyncResult):
        """SUCCESS means that there was a normal return."""
        id_type = 'arxiv'
        paper_id = '1234.5678'
        mock_AsyncResult.return_value = mock.MagicMock(
            status='SUCCESS',
            result={'paper_id': paper_id, 'id_type': id_type}
        )
        task = extract.get_extraction_task(paper_id, 'arxiv')
        self.assertEqual(task.status, ExtractionTask.Statuses.SUCCEEDED)
        self.assertEqual(task.paper_id, paper_id)
        self.assertEqual(task.id_type, id_type)


class TestExtractFulltext(TestCase):
    """Tests for :func:`extract.extract_fulltext` (the real meat)."""

    @mock.patch(f'{extract.__name__}.store.store', mock.MagicMock())
    @mock.patch(f'{extract.__name__}.pdf.retrieve')
    def test_pdf_does_not_exist(self, mock_retrieve):
        """We screwed up, and created a task for a non-existant PDf."""
        document_id = '1234.56789'
        pdf_url = f'https://arxiv.org/pdf/{document_id}'
        mock_retrieve.side_effect = pdf.DoesNotExist
        with self.assertRaises(RuntimeError):
            extract.extract_fulltext(document_id, pdf_url)
