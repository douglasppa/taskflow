import TaskForm from './TaskForm';
import type { TaskFormData } from './TaskForm';
import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useState } from 'react';

interface TaskFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: TaskFormData) => void;
  initialData?: TaskFormData;
  editMode?: boolean;
}

export default function TaskFormModal({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  editMode = false,
}: TaskFormModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFormSubmit = async (data: TaskFormData) => {
    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-40" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-md bg-white p-6 shadow-xl transition-all">
                <Dialog.Title className="text-lg font-bold mb-4">
                  {editMode ? 'Editar Tarefa' : 'Nova Tarefa'}
                </Dialog.Title>

                <TaskForm
                  onSubmit={handleFormSubmit}
                  initialData={initialData}
                  isSubmitting={isSubmitting}
                />

                <button
                  onClick={onClose}
                  className="mt-4 text-sm text-gray-600 hover:underline"
                  disabled={isSubmitting}
                >
                  Cancelar
                </button>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
