import React from "react";
import { Modal, Button } from "flowbite-react";
import { CheckCircleIcon, XCircleIcon, InformationCircleIcon } from "@heroicons/react/20/solid";

function AlertModal({
  isOpen,
  onClose,
  type,
  message = "An error occurred.",
  buttonText = "OK",
}) {
  let modalStyle = "bg-green-500"; // Default success style
  let icon = <CheckCircleIcon className="h-12 w-12" />; // Success icon

  if (type === "error") {
    modalStyle = "bg-red-500";
    icon = <XCircleIcon className="h-12 w-12 text-red-500" />; // Error icon
  }

  if (type === "advice") {
    modalStyle = "bg-yellow-500";
    icon = <InformationCircleIcon className="h-12 w-12" />; // Advice icon
  }

  return (
    <Modal
      show={isOpen}
      size="md"
      popup={true}
      onClose={onClose}
      className="backdrop-blur-sm"
    >
      <Modal.Header />
      <Modal.Body>
        <div className="text-center">
          <div className="flex justify-center mb-4">
            {icon}
          </div>
          <h3 className="text-lg font-medium">{message}</h3>
          <div className="mt-5 flex justify-center">
            <Button
              onClick={onClose}
              className={`${modalStyle} hover:${modalStyle.replace("500", "600")}`}
            >
              {buttonText}
            </Button>
          </div>
        </div>
      </Modal.Body>
    </Modal>
  );
}

export default AlertModal;
