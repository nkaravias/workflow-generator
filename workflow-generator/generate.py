from parser import create_parser
from workflow_manager import WorkflowManager
from logger import workflow_logger


def create_workflow(args):
    changed_files = [
        "/resource_config/projects/001/nonp/abc.yaml",
        "/resource_config/projects/002/nonp/xyz.yaml",
        "/platform_config/projects/003/nonp/123.yaml",
        "/platform_config/projects/004/nonp/test.yaml",
        "/platform_config/projects/006/test/secret.yaml",
        "/platform_config/org/lala.yaml"
    ]

    workflow_template_path = "../workflow_template_test.yaml"
    workflow_manager = WorkflowManager(workflow_template_path, changed_files)
    workflow = workflow_manager.generate_workflow()

    with open(args.output_file, 'w') as f:
        f.write(workflow.to_yaml())


def mock_workflow(args):
    print(args)
    workflow_template_path = "../workflow_template_test.yaml"
    workflow_manager = WorkflowManager(workflow_template_path, [])
    workflow = workflow_manager.mock_workflow()

    with open(args.output_file, 'w') as f:
        f.write(workflow.to_yaml())


def validate_trigger(args):
    # Perform trigger validation
    pass


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'workflow':
        if args.workflow_command == 'create':
            create_workflow(args)
        elif args.workflow_command == 'mock':
            mock_workflow(args)
        else:
            print("Invalid workflow command.")
    elif args.command == 'trigger':
        if args.trigger_command == 'validate':
            validate_trigger(args)
        else:
            print("Invalid trigger command.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()