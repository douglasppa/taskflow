import TaskForm from './TaskForm';
import type { TaskFormData } from './TaskForm';
import {
  Dialog,
  Transition,
  TransitionChild,
  DialogPanel,
  DialogTitle,
} from '@headlessui/react';
import { Fragment, useState } from 'react';

interface TaskFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: TaskFormData) => Promise<void>;
  initialData?: TaskFormData;
  editMode?: boolean;
}

export default function TaskFormModal({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  editMode = false,
}: Readonly<TaskFormModalProps>) {
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
        <TransitionChild
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-40" />
        </TransitionChild>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <TransitionChild
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <DialogPanel className="w-full max-w-md transform overflow-hidden rounded-md bg-white p-6 shadow-xl transition-all">
                <DialogTitle className="text-lg font-bold mb-4">
                  {editMode ? 'Editar Tarefa' : 'Nova Tarefa'}
                </DialogTitle>

                <TaskForm
                  onSubmit={handleFormSubmit}
                  onCancel={onClose}
                  initialData={initialData}
                  isSubmitting={isSubmitting}
                />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
